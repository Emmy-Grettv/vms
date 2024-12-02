from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Time
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase
from sqlalchemy.exc import IntegrityError
from faker import Faker
import random
from datetime import datetime, timedelta
import string
from models import Volunteer, Event, Participation

DATABASE_URL = "postgresql://postgres:123@localhost/testdb"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

class Base(DeclarativeBase):
    pass

# SessionLocal for creating sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize Faker for generating fake data
fake = Faker()

# Function to generate random string for name and email
def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Generate Events
def generate_events(num_events):
    events = []
    for _ in range(num_events):
        event = Event(
            name=fake.sentence(nb_words=4),
            description=fake.text(max_nb_chars=200),
            location=fake.city(),
            date=fake.date_this_year(),
            time=fake.time()
        )
        events.append(event)
    return events

# Generate Volunteers
def generate_volunteers(num_volunteers):
    volunteers = []
    for _ in range(num_volunteers):
        volunteer = Volunteer(
            name=fake.name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            age=random.randint(18, 70),
            skills=fake.job()
        )
        volunteers.append(volunteer)
    return volunteers

# Generate Participations (Schedules)
def generate_participations(volunteers, events, num_participations):
    participations = []
    for _ in range(num_participations):
        participation = Participation(
            volunteer_id=random.choice(volunteers).volunteer_id,
            event_id=random.choice(events).event_id,
            role=fake.job(),
            status="Confirmed",
            date_joined=fake.date_this_year()
        )
        participations.append(participation)
    return participations

# Insert Data in Batches
def insert_data_in_batches(session, data, batch_size=1000):
    for i in range(0, len(data), batch_size):
        session.bulk_save_objects(data[i:i + batch_size])
        session.commit()

# Main Function
def main():
    # Use a database session
    db = SessionLocal()

    try:
        print("Generating events...")
        events = generate_events(5000)  # Generate 5,000 events
        print("Generating volunteers...")
        volunteers = generate_volunteers(5000)  # Generate 5,000 volunteers
        print("Generating participations (schedules)...")
        participations = generate_participations(volunteers, events, 5000)  # Generate 5,000 participations

        # Insert events, volunteers, and participations into the database
        insert_data_in_batches(db, events)
        insert_data_in_batches(db, volunteers)
        insert_data_in_batches(db, participations)

        print(f"Inserted {len(events)} events.")
        print(f"Inserted {len(volunteers)} volunteers.")
        print(f"Inserted {len(participations)} participations.")

        print("Data population completed!")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
