#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Dev, Freebie

if __name__ == "__main__":
    engine = create_engine('sqlite:///freebies.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Clear existing data
    session.query(Freebie).delete()
    session.query(Dev).delete()
    session.query(Company).delete()
    session.commit()
    

    # Create companies
    google = Company(name="Google", founding_year=1998)
    microsoft = Company(name="Microsoft", founding_year=1975)
    apple = Company(name="Apple", founding_year=1976)
    meta = Company(name="Meta", founding_year=2004)

    session.add_all([google, microsoft, apple, meta])
    session.commit()

    # Create devs
    alex = Dev(name="Alex")
    jordan = Dev(name="Jordan")
    taylor = Dev(name="Taylor")
    morgan = Dev(name="Morgan")

    session.add_all([alex, jordan, taylor, morgan])
    session.commit()

    # Create freebies
    freebies = [
        # Alex's freebies
        Freebie(item_name="T-shirt", value=20, dev=alex, company=google),
        Freebie(item_name="Stickers", value=5, dev=alex, company=microsoft),
        
        # Jordan's freebies
        Freebie(item_name="Hoodie", value=45, dev=jordan, company=meta),
        Freebie(item_name="Water Bottle", value=15, dev=jordan, company=apple),
        
        # Taylor's freebies
        Freebie(item_name="Backpack", value=35, dev=taylor, company=google),
        Freebie(item_name="Mousepad", value=10, dev=taylor, company=microsoft),
        
        # Morgan's freebies
        Freebie(item_name="Headphones", value=50, dev=morgan, company=apple),
        Freebie(item_name="Notebook", value=8, dev=morgan, company=meta)
    ]

    session.add_all(freebies)
    session.commit()

    print("Database has been seeded!")