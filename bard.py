from bardapi import BardCookies

api = 'bAj0VRACzUfA39PRAyRcAJIkMQKWJMWtE4xszYlHpUFXydcQ52npIhRyLuZt14rjYczvwQ.'
cookie_dict = {
    "__Secure-1PSID": "bAj0VRACzUfA39PRAyRcAJIkMQKWJMWtE4xszYlHpUFXydcQ52npIhRyLuZt14rjYczvwQ.",
    "__Secure-1PSIDTS": "sidts-CjIB3e41hVvV9zLnenCADVI0FnnUhXjN-emS1SmX3gFBVWNZAOpS187OWCaLyEtIsQTn5hAA",
    # Any cookie values you want to pass session object.
}

#bard =Bard(token=api)
bard = BardCookies(cookie_dict=cookie_dict)

result = bard.get_answer("Who is ceo of google")
print(result['content'])