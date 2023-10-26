from datetime import datetime, timedelta
from .models.donations import Donation
from .extensions import db


def update_next_donation_dates():
    recurring_donations = Donation.query.filter(Donation.is_recurring.is_(True)).all()

    for donation in recurring_donations:
        if donation.frequency == "monthly":
            donation.next_donation_date += timedelta(days=30)
        elif donation.frequency == "quarterly":
            donation.next_donation_date += timedelta(days=90)

    db.session.commit()
