import boto
import mongoengine as me
#import jinja2 as jinja

import rmc.models as m
import rmc.shared.constants as c
import rmc.shared.secrets as secrets

me.connect(c.MONGO_DB_RMC)

def send_exam_schedule_email():

    conn = boto.connect_ses(
        aws_access_key_id=secrets.AWS_KEY_ID,
        aws_secret_access_key=secrets.AWS_SECRET_KEY)

    # TODO(mack): come up with name for email
    EMAIL_TITLE = 'Welcome to Flow'

    # TODO(mack): should not show num_friends if it's 0
    email_body = \
"""Hey %(first_name)s!

Thanks for signing up for Flow! We're really excited to have you on board.

Did you know %(num_friends)d friends have also signed up and are using Flow to plan, track and discover new courses!

Also, Flow now lets you see your final exam schedule for this term! Check if out on your profile at: http://uwflow.com/profile. (Don't worry, we'll continue to update it, so you don't have too!)

We're working hard to bring you more awesome features! Stay connected with us on Facebook (http://www.facebook.com/planyourflow) and Twitter (https://twitter.com/useflow).

Much love,

The Flow Team."""

    # TODO(mack): .only()
    #users = m.User.objects(
    #    sent_exam_schedule_notifier_email=False,
    #    email__exists=True,
    #)
    users = m.User.objects(
        fbid='1647810326',
        sent_exam_schedule_notifier_email=False,
        email__exists=True,
    )

    num_sent = 0
    for user in users:
        try:
            params = {
                'first_name': user.first_name,
                'num_friends': len(user.friend_ids),
            }
            conn.send_email(
                c.EMAIL_SENDER,
                EMAIL_TITLE,
                email_body % params,
                [user.email],
            )
            user.sent_exam_schedule_notifier_email = True
            user.save()
            num_sent += 1
        except:
            print 'Could not send email to user: %s' % user.id

    print 'Sent email to %d users' % num_sent

if __name__ == '__main__':
    send_exam_schedule_email()
