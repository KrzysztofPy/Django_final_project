from faker import Factory

from appointment_app.models import User, PhysicianSpeciality, PHYSICIAN_SPECIALITIES

NUMBER_OF_USERS = 25
NUMBER_OF_DOCTORS = 15


def create_name():
    fake = Factory.create()
    first_name = fake.first_name()
    last_name = fake.last_name()
    return first_name, last_name


def create_patients():
    for patient in range(0, NUMBER_OF_USERS):
        first_name, last_name = create_name()
        User.objects.create(name=first_name,
                            surname=last_name,
                            email=f"{first_name}{last_name[0]}@djangoMED.com",
                            login=f"{first_name}_{last_name}"
                            )

"""
def create_physician_speciality():
    fake = Factory.create("en_EN")
    for _, speciality in PHYSICIAN_SPECIALITIES:
        PhysicianSpeciality.objects.create(name=speciality,
                                           description=fake.text()
                                          )

def create_subjects():
    Subject.objects.create(name="Język polski", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Matematyka", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Język angielski", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Fizyka", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Wychowanie fizyczne", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Technika", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Biologia", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Chemia", teacher_name=" ".join(create_name()))
    Subject.objects.create(name="Geografia", teacher_name=" ".join(create_name()))
    """

