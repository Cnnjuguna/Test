from app import create_app, db
from .models.admins import Admin
from .models.admins import Admin
from .models.beneficiaries import Beneficiary
from .models.charities import Charity
from .models.charity_applications import CharityApplications
from .models.donations import Donation
from .models.donors import Donor
from .models.stories import Story
from .models.users import User
from werkzeug.security import generate_password_hash

# Create the Flask app
app = create_app()

# Initialize the database
with app.app_context():
    db.create_all()

    # Create a sample admin
    admin = Admin(user_id=1)
    db.session.add(admin)

    # Create sample users (charity, donor, and admin)
    charity_user = User(
        username="charity_user",
        email="charity@example.com",
        password=generate_password_hash("password"),
        role="charity",
    )
    donor_user = User(
        username="donor_user",
        email="donor@example.com",
        password=generate_password_hash("password"),
        role="donor",
    )
    admin_user = User(
        username="admin_user",
        email="admin@example.com",
        password=generate_password_hash("password"),
        role="admin",
    )
    db.session.add(charity_user)
    db.session.add(donor_user)
    db.session.add(admin_user)
    db.session.commit()

    # Create sample beneficiaries
    beneficiary1 = Beneficiary(
        charity_id=1, name="Beneficiary 1", description="Description 1"
    )
    beneficiary2 = Beneficiary(
        charity_id=1, name="Beneficiary 2", description="Description 2"
    )
    db.session.add(beneficiary1)
    db.session.add(beneficiary2)

    # Create sample charities
    charity = Charity(name="Sample Charity", admin_id=1, total_donation_amount=0)
    db.session.add(charity)

    # Create sample charity applications
    charity_app = CharityApplications(charity_id=1, admin_id=1, status="approved")
    db.session.add(charity_app)

    # Create sample donations
    donation = Donation(
        donor_id=1,
        charity_id=1,
        amount=100,
        admin_id=1,
        donation_frequency="monthly",
        total_donation_amount=100,
    )
    db.session.add(donation)

    # Create sample donors
    donor = Donor(user_id=3, name="Sample Donor", donation_frequency="monthly")
    db.session.add(donor)

    # Create sample stories
    story = Story(
        charity_id=1,
        title="Beneficiary Story",
        content="This is a beneficiary story",
        status="published",
    )
    db.session.add(story)

    db.session.commit()
