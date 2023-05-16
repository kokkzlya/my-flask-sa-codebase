from gevent import monkey

monkey.patch_all()

if __name__ == "__main__":
    import fire
    from myproject.cli.cli import CLI
    fire.Fire(CLI())
