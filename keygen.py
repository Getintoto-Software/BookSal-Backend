from vapid import Vapid

vapid = Vapid()
vapid.generate_keys()

public_key = vapid.public_key().decode('utf-8')
private_key = vapid.private_key().decode('utf-8')

print('VAPID_PUBLIC_KEY:', public_key)
print('VAPID_PRIVATE_KEY:', private_key)
