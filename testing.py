import email_service
import requests
FLASK_TEST_ADDR = 'http://127.0.0.1:5000/email'


def request_builder(to_addr, to_name, from_addr, from_name, subject="Hi", body="What's up"):
	return {
		"to": to_addr, 
		"to_name": to_name,
		"from": from_addr, 
		"from_name": from_name,
		"subject": subject,
		"body": body
	}

def test_email_service():
	# Test: Fake email sender.
	test_request1 = request_builder("fake", "Mr. Fake", "noreply@mybrightwheel.com", "Brightwheel", "A Message from Brighwheet", "<h1>Your Bill</h><p>$10</p>")
	r1 = requests.post(FLASK_TEST_ADDR, data = test_request1)
	print(r1.text)

	# Test: Email sender is email recipient.
	test_request2 = request_builder("jpicar@berkeley.edu", "Justin Picar", "jpicar@berkeley.edu", "Justin Picar", "To yourself, part 1.", "<h1>Your Bill</h><p>$10</p>")
	r2 = requests.post(FLASK_TEST_ADDR, data = test_request2)
	print(r2.text)

	# Test: Sending to multiple emails.
	test_request3 = request_builder(["jpicar@berkeley.edu", "picar.justin@gmail.com"], ["Justin Picar", "Picar Justin"], "jpicar@berkeley.edu", "Justin Picar", "To yourself, part 2.", "<h1><a href='https://google.com'>Google</a> says:</h><p>Formatting</p><p>Is</p><p>Important</p>.")
	r3 = requests.post(FLASK_TEST_ADDR, data = test_request3)
	print(r3.text)

	# Test: Body is an invalid type.
	test_request4 = request_builder("jpicar@berkeley.edu", "Justin Picar", "jpicar@berkeley.edu", "Justin Picar", "To yourself, part 3.", 12345)
	r4 = requests.post(FLASK_TEST_ADDR, data = test_request4)
	print(r4.text)

	# Test: Subject, but empty body.
	test_request5 = request_builder("jpicar@berkeley.edu", "Justin Picar", "jpicar@berkeley.edu", "Justin Picar", "To yourself, part 4.", "")
	r5 = requests.post(FLASK_TEST_ADDR, data = test_request5)
	print(r5.text)

test_email_service()