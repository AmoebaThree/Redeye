import systemd.daemon
import initio
import redis
import RPi.GPIO as GPIO
import sys


def execute():
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
    redis_queue_left = redis_queue + '.left'
    redis_queue_right = redis_queue + '.right'

    message_left_off = message_prefix + '.left.off'
    message_left_on = message_prefix + '.left.on'
    message_right_off = message_prefix + '.right.off'
    message_right_on = message_prefix + '.right.on'

    r = redis.Redis(host='192.168.0.1', port=6379,
                    db=0, decode_responses=True)
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe(redis_queue)

    r.publish('services', redis_queue + '.on')
    systemd.daemon.notify('READY=1')
    print('Startup complete')

    try:
        def left_callback(c):
            if GPIO.input(left_sensor):
                r.publish(redis_queue_left, message_left_off)
            else:
                r.publish(redis_queue_left, message_left_on)

        def right_callback(c):
            if GPIO.input(right_sensor):
                r.publish(redis_queue_right, message_right_off)
            else:
                r.publish(redis_queue_right, message_right_on)

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

        r.publish('services', redis_queue + '.off')
        print('Goodbye')


if __name__ == '__main__':
    execute()
