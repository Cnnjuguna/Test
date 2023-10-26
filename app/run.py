from app import create_app
from scheduler import scheduler

app = create_app()

if __name__ == "__main__":
    # Starting the scheduler
    scheduler.run()  # We run scheduler in the same process
    app.run(debug=True)
