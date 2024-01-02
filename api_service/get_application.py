application = None


def get_application():
    global application
    if not application:
        from application import Application

        application = Application()
    return application
