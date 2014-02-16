from firstaidkit import *
auth.User.create_table(fail_silently=True)  # make sure table created.
admin = auth.User(username='admin', email='', admin=True, active=True)
admin.set_password('admin')
admin.save()

Person.create_table(fail_silently=True)

# create person records
p = Person.create(firstname="Fred", lastname="Prieur", title="Dr")
p.save()

# create about records
About.create_table(fail_silently=True)

# create section records
Section.create_table(fail_silently=True)
s = Section.create(title="Innovate",
                   description="Equipment")
s.save()
s = Section.create(title="Explore",
                   description="Research")
s.save()

s = Section.create(title="Inspire",
                  description="Teaching")
s.save()

s = Section.create(title="Care",
                   description="Patien Care")

s.save()

# create project records
Project.create_table(fail_silently=True)
p = Project.create(title="RINGETTE Gives Back Charity Game: Sharon Rothwell",
                   name="Ringette",
                   person = 1,
                   section = 1,
                   description="The ringette is a beautiful thing for fundraising",
                   amountGoal="500",
                   amountFunded="50",
                   thumbnail="http://placehold.it/300x200")
p.save()

p = Project.create(title="Portable dopplers",
                   name="Portable dopplers",
                   person = 1,
                   section = 1,
                   description="my description",
                   amountGoal="1262",
                   amountFunded="1100",
                   thumbnail="http://placehold.it/300x200")
p.save()

