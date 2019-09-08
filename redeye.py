if __name__ == '__main__':
    import systemd.daemon, initio, redis, RPi.GPIO as GPIO

    print('Startup')
    initio.init(IR=True)
    r = redis.Redis(host='192.168.0.1', port=6379, db=0)
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe('redeye')
    print('Startup complete')
    systemd.daemon.notify('READY=1')

    try:
        def left_callback(c):
            if GPIO.input(initio.irFL):
                r.publish("redeye-left", "left-off")
            else:
                r.publish("redeye-left", "left-on")
        def right_callback(c):
            if GPIO.input(initio.irFR):
                r.publish("redeye-right", "right-off")
            else:
                r.publish("redeye-right", "right-on")

        GPIO.add_event_detect(initio.irFL, GPIO.BOTH, callback=left_callback, bouncetime=100)  
        GPIO.add_event_detect(initio.irFR, GPIO.BOTH, callback=right_callback, bouncetime=100)  
        left_callback(initio.irFL)
        right_callback(initio.irFR)

        for message in p.listen():
            # If message is received, send current status
            left_callback(initio.irFL)
            right_callback(initio.irFR)

    except:
        p.close()
        initio.cleanup()
        print("Goodbye")