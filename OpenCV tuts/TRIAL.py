account_sid = 'AC6ca3ae3b9b261f50b22a64aa40567bc7'
auth_token = '[AuthToken]'
client = Client(account_sid, auth_token)

verification = client.verify \
    .v2 \
    .services('VA96fafbf7eab7629dc35f8362de345363') \
    .verifications \
    .create(to='+919548891174', channel='sms')

print(verification.sid)