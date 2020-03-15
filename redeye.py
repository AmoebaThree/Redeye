if __name__ == '__main__':
    import systemd.daemon
    import initio
    import redis
    import RPi.GPIO as GPIO
    import sys

    print('Startup')
    if len(sys.argv) > 1 and sys.argv[1] == 'line':
        print('Line mode')
        initio.init(Line=True)
        message_prefix = 'line'
        left_sensor = initio.lineLeft
        right_sensor = initio.lineRight
    else:
        print('Obstacle mode')
        initio.init(IR=True)
        message_prefix = 'obstacle'
        left_sensor = initio.irFL
        right_sensor = initio.irFR

    redis_queue = 'redeye.' + message_prefix
    r = redis.Redis(host='192.168.0.1', port=6379,
                    db=0, decode_responses=True)
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe(redis_queue)
    print('Startup complete')
    systemd.daemon.notify('READY=1')

    try:
        def left_callback(c):
            if GPIO.input(left_sensor):
                r.publish(redis_queue + '.left', message_prefix + '.left.off')
            else:
                r.publish(redis_queue + '.left', message_prefix + '.left.on')

        def right_callback(c):
            if GPIO.input(right_sensor):
                r.publish(redis_queue + '.right',
                          message_prefix + '.right.off')
            else:
                r.publish(redis_queue + '.right', message_prefix + '.right.on')

        GPIO.add_event_detect(left_sensor, GPIO.BOTH,
                              callback=left_callback, bouncetime=100)
        GPIO.add_event_detect(right_sensor, GPIO.BOTH,
                              callback=right_callback, bouncetime=100)
        left_callback(left_sensor)
        right_callback(right_sensor)

        for message in p.listen():
            # If message is received, send current status
            left_callback(left_sensor)
            right_callback(right_sensor)

    except:
        p.close()
        initio.cleanup()
        print('Goodbye')
