#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import random
import argparse

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parse_arguments(args):
    """Parse the command line arguments for the console commands.
    Args:
      args (List[str]): List of string arguments to be parsed.
    Returns:
      Namespace: Namespace with the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='Auto-Change PTC Account Password'
    )
    parser.add_argument(
        '-f', '--file', type=str, default=None, required=True,
        help='File of accounts to check (RocketMap csv format or txt format).'
    )
    parser.add_argument(
        '-pw', '--password', type=str, default=None, required=True,
        help='New password for PTC account (8 to 50 characters, containing uppercase, lowercase, numbers and symbols).'
    )

    return parser.parse_args(args)


def setup():

   # Set chrome to incognito mode
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--incognito')

    # Load chrome options
    driver = webdriver.Chrome(executable_path=r'chromedriver',
                              chrome_options=chrome_options)

    driver.set_window_position(0, 0)
    driver.set_window_size(800, 600)

    return driver


def login(username, password, driver=None):

    # Navigate to the login page
    driver.get('https://www.pokemon.com/us/pokemon-trainer-club/caslogin'
               )
    timeout = random.uniform(15, 30)  # seconds

    driver.find_element_by_name('username').send_keys(username)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('Login').click()

    return driver


def check_password(password):

    pass


def change_password(driver, cur_password, new_password, edit_profile_xpath):

    # Click "Edit Profile"
    edit_profile = driver.find_element_by_xpath(edit_profile_xpath)
    edit_profile.click()

    # Click "Change Password"
    change_password_xpath = \
        '//*[@id="account"]/fieldset[1]/div/div/a[2]'
    change_password = \
        driver.find_element_by_xpath(change_password_xpath)
    change_password.click()

    # Set new password
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,
                         'form-field')))
    cur_password_btn = driver.find_element_by_name('current_password')
    new_password_btn = driver.find_element_by_name('password')
    confirm_password_btn = \
        driver.find_element_by_name('confirm_password')

    change_btn = \
        driver.find_element_by_xpath('//*[@id="account"]/input[2]')

    cur_password_btn.send_keys(cur_password)
    new_password_btn.send_keys(new_password)
    confirm_password_btn.send_keys(new_password)
    change_btn.click()

    return driver


def append_to_file(username, password, filename):
    if os.path.exists(filename):
        f = open('./' + filename, 'a+b')
    else:
        f = open('./' + filename, 'w+b')

    f.write('ptc,' + username + ',' + password + '\n')

    f.close()


if __name__ == '__main__':

    #new_password = 'ABCD!DCBA'
    #accounts_file = 'acc.csv'
    args = parse_arguments(sys.argv[1:])
    accounts_file = args.file
    new_password = args.password
    
    # default files to save
    success_file = 'succeed.csv'
    failed_file = 'failed.csv'

    # format of accounts_file can be: [ptc,username,password] or [username:password]
    with open(accounts_file, 'r') as f:
        success_count = 0
        for line in f:
            contents = re.split('[,:]', line.rstrip('\n'))
            cur_password = contents[-1]
            username = contents[-2]

            # Check if the password is same as the target one.
            if cur_password == new_password:
                print('{}: no need to change password.'.format(username))
                append_to_file(username, cur_password, success_file)
            else:
                driver = login(username, cur_password, setup())
                # Check if the login successes.
                try:
                    wait = WebDriverWait(driver, 5)
                    edit_profile_xpath = \
                        '/html/body/div[3]/section[2]/div[1]/ul[2]/li[1]/div/a/h3'
                    element = \
                        wait.until(EC.element_to_be_clickable((By.XPATH,
                                   edit_profile_xpath)))
                    change_password(driver, cur_password, new_password,
                                    edit_profile_xpath)
                    # Check if the password is successfully changed.
                    try:
                        wait = WebDriverWait(driver, 5)
                        confirmation_xpath = \
                            '/html/body/div[3]/section[2]/div/h2'
                        element = \
                            wait.until(EC.element_to_be_clickable((By.XPATH,
                                   confirmation_xpath)))
                        
                        append_to_file(username, new_password, success_file)
                        success_count += 1
                        print('Successfully changed password for {} (#{}).'.format(username, success_count))
                    except TimeoutException:  # Usually due to bad new password.
                        append_to_file(username, cur_password, failed_file)
                        print('Failed to change password for {} (bad new password).'.format(username))
                        pass
                except TimeoutException:  # Usually due to wrong login password.
                    append_to_file(username, cur_password, failed_file)
                    print('Failed to change password for {} (bad login).'.format(username))
                    pass
                driver.close()
    f.close()

    print('Done...')

    driver.quit()
