class TestLength:
    def test_length(self):
        phrase = input("Set a phrase: ")
        length_phrase = len(phrase)
        assert length_phrase > 0, "No phrase was entered. The input cannot be empty."
        assert length_phrase < 15, f"The length is {length_phrase}, but should be less than 15 "