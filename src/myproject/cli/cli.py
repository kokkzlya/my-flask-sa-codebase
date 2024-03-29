class CLI(object):
    def run_dev(self):
        from myproject.wsgi import app
        app.run(host="0.0.0.0", port=5000, debug=True)

    def run_web(self):
        """
        Run the web application in production
        """
        _execvp([
            "gunicorn",
            "--config", "python:myproject.gunicorn_cfg",
            "myproject.wsgi:app",
        ])

    def run_healthcheck(self):
        """
        Run healthcheck
        """
        import requests

        resp = requests.get(
            "http://myproject.127.0.0.1.nip.io:5000/healthcheck",
        )
        print(resp.text)
        raise SystemExit(0 if resp.status_code < 300 else 1)


def _execvp(args):
    import os
    os.execvp(args[0], args)
