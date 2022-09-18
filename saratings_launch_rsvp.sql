select title,first_name,last_name,email_address,contact_number,company,confirm_attendance as 'confirmed_attendance',
date(rsvp_date) as rsvp_date from event_rsvp
order by last_name