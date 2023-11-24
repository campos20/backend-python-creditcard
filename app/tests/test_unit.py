from app.helper.hash_helper import hash_all_but_last_n_chars


def test_hash_credit_card():
    start = "asdfghjkl"
    end = "qwer"
    to_hash = start + end
    visible_count = len(end)
    expected_hash = "X" * len(start) + end
    assert expected_hash == hash_all_but_last_n_chars(to_hash, visible_count)
