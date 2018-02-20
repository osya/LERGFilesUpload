# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
import datetime as dt
import os
import os.path as op

from flask import url_for
from webtest import Upload


class TestLoggingIn:
    """Login."""

    def test_can_log_in_returns_302(self, user, testapp):
        """Login successful."""
        # Goes to homepage
        res = testapp.get('/')
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        assert res.status_code == 302

    def test_sees_alert_on_log_out(self, user, testapp):
        """Show alert on logout."""
        res = testapp.get('/')
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        # Submits
        form.submit().follow()
        res = testapp.get(url_for('public.logout')).follow()
        # sees alert
        assert 'You are logged out.' in res

    def test_sees_error_message_if_password_is_incorrect(self, user, testapp):
        """Show error if password is incorrect."""
        # Goes to homepage
        res = testapp.get('/')
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'wrong'
        # Submits
        res = form.submit()
        # sees error
        assert 'Invalid password' in res

    def test_sees_error_message_if_username_doesnt_exist(self, user, testapp):
        """Show error if username doesn't exist."""
        # Goes to homepage
        res = testapp.get('/')
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = 'unknown'
        form['password'] = 'myprecious'
        # Submits
        res = form.submit()
        # sees error
        assert 'Unknown user' in res


# Register endpoint commented due this app intended only for admins. All other users will only use public API
# class TestRegistering:
#     """Register a user."""
#
#     def test_can_register(self, user, testapp):
#         """Register a new user."""
#         old_count = len(User.query.all())
#         # Goes to homepage
#         res = testapp.get('/')
#         # Clicks Create Account button
#         res = res.click('Create account')
#         # Fills out the form
#         form = res.forms['registerForm']
#         form['username'] = 'foobar'
#         form['email'] = 'foo@bar.com'
#         form['password'] = 'secret'
#         form['confirm'] = 'secret'
#         # Submits
#         res = form.submit().follow()
#         assert res.status_code == 200
#         # A new user was created
#         assert len(User.query.all()) == old_count + 1
#
#     def test_sees_error_message_if_passwords_dont_match(self, user, testapp):
#         """Show error if passwords don't match."""
#         # Goes to registration page
#         res = testapp.get(url_for('public.register'))
#         # Fills out form, but passwords don't match
#         form = res.forms['registerForm']
#         form['username'] = 'foobar'
#         form['email'] = 'foo@bar.com'
#         form['password'] = 'secret'
#         form['confirm'] = 'secrets'
#         # Submits
#         res = form.submit()
#         # sees error message
#         assert 'Passwords must match' in res
#
#     def test_sees_error_message_if_user_already_registered(self, user, testapp):
#         """Show error if user already registered."""
#         user = UserFactory(active=True)  # A registered user
#         user.save()
#         # Goes to registration page
#         res = testapp.get(url_for('public.register'))
#         # Fills out form, but username is already registered
#         form = res.forms['registerForm']
#         form['username'] = user.username
#         form['email'] = 'foo@bar.com'
#         form['password'] = 'secret'
#         form['confirm'] = 'secret'
#         # Submits
#         res = form.submit()
#         # sees error
#         assert 'Username already registered' in res


def login_and_upload(testapp, user):
    res = testapp.get('/')
    form = res.forms['loginForm']
    form['username'] = user.username
    form['password'] = 'myprecious'
    form.submit().follow()

    res = testapp.get(url_for('lerg.upload'))
    form = res.forms['uploadForm']
    filename = op.abspath(
        op.join(testapp.app.config['PROJECT_ROOT'], os.pardir, 'Jurisdiction_OCN_LATA_ABLock_Upload_2016-05-9 (2).csv'))
    form['file_upload'] = Upload(filename)
    return form.submit()


class TestFileUploading:
    """LERG File uploading."""

    def test_file_uploading(self, user, testapp):
        res = login_and_upload(testapp, user)
        assert res.status_code == 200


class TestAPI:
    """Testing API."""

    def test_get_last_refresh(self, testapp, db):
        res = testapp.get(url_for('lerg.get_last_refresh'))
        assert res.status_code == 200

    def test_upload_and_get_last_refresh(self, testapp, user):
        login_and_upload(testapp, user)
        res = testapp.get(url_for('lerg.get_last_refresh'))
        assert 'last_refresh_date' in res.json_body and res.json_body['last_refresh_date'] is not None

    def test_get_lerg(self, testapp, db):
        date = dt.datetime.utcnow().date() + dt.timedelta(days=1)
        url = url_for('lerg.get_lerg', date=date)
        res = testapp.get(url, status=404)
        assert res.status_code == 404

    def test_upload_and_get_lerg(self, testapp, user):
        login_and_upload(testapp, user)
        date = dt.datetime.utcnow().date() + dt.timedelta(days=1)
        url = url_for('lerg.get_lerg', date=date)
        res = testapp.get(url)
        assert res.status_code == 200 and res.content_length > 0

    def test_get_lerg_by_cnt_state(self, testapp, db):
        date = dt.datetime.utcnow().date() + dt.timedelta(days=1)
        url = url_for('lerg.get_lerg_by_cnt_state', date=date)
        res = testapp.get(url, status=404)
        assert res.status_code == 404

    def test_upload_and_get_lerg_by_cnt_state(self, testapp, user):
        login_and_upload(testapp, user)
        date = dt.datetime.utcnow().date() + dt.timedelta(days=1)
        url = url_for('lerg.get_lerg_by_cnt_state', date=date)
        res = testapp.get(url)
        assert res.status_code == 200 and res.content_length > 0

    def test_get_lerg_by_cnt_state2(self, testapp, db):
        date = dt.datetime.utcnow().date() + dt.timedelta(days=1)
        url = url_for('lerg.get_lerg_by_cnt_state2', date=date)
        res = testapp.get(url, status=404)
        assert res.status_code == 404

    def test_upload_and_get_lerg_by_cnt_state2(self, testapp, user):
        login_and_upload(testapp, user)
        date = dt.datetime.utcnow().date() + dt.timedelta(days=1)
        url = url_for('lerg.get_lerg_by_cnt_state2', date=date)
        res = testapp.get(url)
        assert res.status_code == 200 and res.content_length > 0
