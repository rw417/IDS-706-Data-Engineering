import click

@click.command()
@click.option("--task", prompt="What task would you like to perform", help="Enter name of the task")


def hello(task):
    click.echo(f"Hello, world! I'm new to this world, so I cannot {task} yet... Sorry!")

if __name__ == "__main__":
    hello()