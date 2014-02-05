from firstaidkit import *
auth.User.create_table(fail_silently=True)  # make sure table created.
admin = auth.User(username='admin', email='', admin=True, active=True)
admin.set_password('admin')
admin.save()

Person.create_table(fail_silently=True)
p = Person.create(firstname="Fred", lastname="Prieur", title="Dr")
p.save()
About.create_table(fail_silently=True)
Project.create_table(fail_silently=True)
p = Project.create(title="RINGETTE Gives Back Charity Game: Sharon Rothwell",
                   name="Ringette",
                   description="The ringette is a beautiful thing for fundraising",
                   amountGoal="500",
                   amountFunded="50",
                   thumbnail="http://placehold.it/300x200")
p.save()

