from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'
    
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    
    # Relationship with freebies
    freebies = relationship('Freebie', back_populates='company')
    
    # Relationship with devs through freebies
    devs = relationship('Dev', secondary='freebies', viewonly=True)
    
    def __repr__(self):
        return f'<Company {self.name}>'
    
    def give_freebie(self, dev, item_name, value):
        """
        Takes a dev (an instance of the Dev class), an item_name (string), and a value
        as arguments, and creates a new Freebie instance associated with this company 
        and the given dev.
        """
        new_freebie = Freebie(
            item_name=item_name,
            value=value,
            dev=dev,
            company=self
        )
        return new_freebie
    
    @classmethod
    def oldest_company(cls):
        """
        Returns the Company instance with the earliest founding year
        """
        from sqlalchemy.orm import Session
        from sqlalchemy import create_engine
        
        engine = create_engine('sqlite:///freebies.db')
        session = Session(engine)
        
        return session.query(cls).order_by(cls.founding_year).first()


class Dev(Base):
    __tablename__ = 'devs'
    
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    
    # Relationship with freebies
    freebies = relationship('Freebie', back_populates='dev')
    
    # Relationship with companies through freebies
    companies = relationship('Company', secondary='freebies', viewonly=True)
    
    def __repr__(self):
        return f'<Dev {self.name}>'
    
    def received_one(self, item_name):
        """
        Accepts an item_name (string) and returns True if any of the freebies 
        associated with the dev has that item_name, otherwise returns False.
        """
        for freebie in self.freebies:
            if freebie.item_name == item_name:
                return True
        return False
    
    def give_away(self, dev, freebie):
        """
        Accepts a Dev instance and a Freebie instance, changes the freebie's dev to 
        be the given dev; only makes the change if the freebie belongs to the dev 
        who's giving it away.
        """
        if freebie in self.freebies:
            freebie.dev = dev
            return True
        return False


class Freebie(Base):
    __tablename__ = 'freebies'
    
    id = Column(Integer(), primary_key=True)
    item_name = Column(String(), nullable=False)
    value = Column(Integer(), nullable=False)
    
    # Foreign Keys
    dev_id = Column(Integer(), ForeignKey('devs.id'), nullable=False)
    company_id = Column(Integer(), ForeignKey('companies.id'), nullable=False)
    
    # Relationships
    dev = relationship('Dev', back_populates='freebies')
    company = relationship('Company', back_populates='freebies')
    
    def __repr__(self):
        return f'<Freebie {self.item_name}>'
    
    def print_details(self):
        """
        Returns a string formatted as follows: 
        {dev name} owns a {freebie item_name} from {company name}.
        """
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}."