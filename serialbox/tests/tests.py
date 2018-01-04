'''
    Copyright 2016 SerialLab, LLC

    This file is part of SerialBox.

    SerialBox is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    SerialBox is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with SerialBox.  If not, see <http://www.gnu.org/licenses/>.
'''
import logging
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from serialbox.utils import get_region_by_machine_name
from serialbox import discovery

logger = logging.getLogger(__name__)


class PoolTests(APITestCase):

    def setUp(self):
        user = User.objects.create_user(username='testuser',
                                   password='unittest',
                                   email='testuser@seriallab.local')
        self.client.force_authenticate(user=user)
        self.create_pool()
        self.create_region()

    def tearDown(self):
        '''
        Get rid of any junk.
        '''
        from serialbox.models import Pool, SequentialRegion
        Pool.objects.all().delete()
        SequentialRegion.objects.all().delete()

    def create_pool(self, data=None, assert_status=status.HTTP_201_CREATED):
        '''
        Ensure we can create a new pool instance.
        '''
        data = data or {
            "readable_name": "created by unit test",
            "machine_name": "utpool1",
            "active": "true",
            "request_threshold": 100
        }
        url = reverse('pool-create')
        response = self.client.post(url, data, format='json')
        logger.debug(response.content)
        self.assertEqual(response.status_code, assert_status)

    def create_region(self, data=None, assert_status=status.HTTP_201_CREATED):
        '''
        Ensure we can create a test region for the created pool instance
        '''
        data = data or {
            "pool": "utpool1",
            "readable_name": "Unit Test Region One",
            "machine_name": "utr1",
            "active": True,
            "order": 1,
            "start": 1,
            "end": 100,
            "state": 0
        }
        url = reverse('sequential-region-create')
        response = self.client.post(url, data, format='json')
        logger.debug(response.content)
        self.assertEqual(response.status_code, assert_status)
        return response

    def modify_region(self, data, machine_name='utr1',
                      assert_status=status.HTTP_200_OK):
        '''
        Ensure we can create a test region for the created pool instance
        '''
        url = reverse('sequential-region-modify', args=[machine_name])
        response = self.client.put(url, data, format='json')
        logger.debug(response.content)
        self.assertEqual(response.status_code, assert_status)
        return response

    def delete_region(self, data, machine_name='utr1',
                      assert_status=status.HTTP_200_OK):
        '''
        Ensure we can create a test region for the created pool instance
        '''
        url = reverse('sequential-region-modify', args=[machine_name])
        response = self.client.delete(url, data, format='json')
        logger.debug(response.content)
        self.assertEqual(response.status_code, assert_status)
        return response

    def test_disable_pool(self):
        '''
        Ensure a disabled pool will not work
        '''
        data = {"active": False,
                "machine_name": "utpool1",
                "readable_name": "Unit Test Pool 1"}
        url = reverse('pool-modify', args=['utpool1'])
        response = self.client.put(url, data, format='json')
        logger.debug(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('allocate-numbers', args=['utpool1', '10'])
        response = self.client.get(url, format='json')
        logger.debug(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_modify_pool(self):
        '''
        Ensure we can update some pool fields.
        '''
        data = {"readable_name": "updated by unit test",
                "machine_name": "utpool1"}
        url = reverse('pool-modify', args=['utpool1'])
        response = self.client.put(url, data, format='json')
        logger.debug(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_regions(self):
        '''
        Ensure we can get the regions by the pool name.
        '''
        regions = discovery.get_all_regions()
        self.assertGreater(len(regions), 0, 'The region count is not greater '
                           'than zero.')

    def test_get_active_regions_by_pool(self):
        '''
        Ensure we can get the regions by the pool name.
        '''
        from serialbox.models import Pool
        pool = Pool.objects.get(machine_name='utpool1')
        regions = discovery.get_all_regions_by_pool(pool)
        logger.debug("Returned %s regions", len(regions))
        self.assertGreater(len(regions), 0, 'The region count is not greater '
                           'than zero.')

    def test_get_pool_size(self):
        from serialbox.models import Pool
        pool = Pool.objects.get(machine_name='utpool1')
        size = discovery.get_total_pool_size(pool)
        self.assertEqual(size, 99, 'The total pool size should be 99.')

    def test_get_all_regions_by_pool(self):
        '''
        Ensure we can get the regions by the pool name even if they are
        marked as inactive.
        '''
        from serialbox.models import Pool, SequentialRegion
        pool = Pool.objects.get(machine_name='utpool1')
        region = SequentialRegion.objects.get(machine_name='utr1')
        region.active = False
        region.save()
        regions = discovery.get_all_regions_by_pool(pool, False)
        logger.debug(regions)
        self.assertGreater(len(regions), 0, 'The region count is not greater '
                           'than zero.')

    def test_allocate_numbers(self):
        '''
        Ensure we can get numbers from the pool
        '''
        url = reverse('allocate-numbers', args=['utpool1', '10'])
        response = self.client.get(url, format='json')
        logger.debug(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_overload_number_request(self):
        '''
        Request too many numbers.
        '''
        url = reverse('allocate-numbers', args=['utpool1', '200'])
        response = self.client.get(url, format='json')
        logger.debug(response.content)
        self.assertEqual(
            response.status_code,
            status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_sequential_region_boundaries(self):
        '''
        Make sure we can't create a region that ovelaps another region
        within the same pool.
        '''
        data = {
            "pool": "utpool1",
            "readable_name": "Unit Test Region One",
            "machine_name": "utr1",
            "active": True,
            "order": 1,
            "start": 50,
            "end": 75,
            "state": 1
        }
        response = self.create_region(
            data,
            assert_status=status.HTTP_400_BAD_REQUEST)
        logger.debug(response.content)

    def test_create_insane_region(self):
        '''
        Try to create a non-sane region that has bad start and end values.
        '''
        data = {
            "pool": "utpool1",
            "readable_name": "Insane Unit Test Region One",
            "machine_name": "iutr1",
            "active": True,
            "order": 1,
            "start": 75,
            "end": 50,
            "state": 1
        }
        response = self.create_region(
            data,
            assert_status=status.HTTP_400_BAD_REQUEST)
        logger.debug(response.content)

    def test_create_overlapping_region(self):
        '''
        Create a region that overlaps another one.
        '''
        bad_data = {
            "pool": "utpool1",
            "readable_name": "Overlapping Unit Test Region Two",
            "machine_name": "outr2",
            "active": True,
            "order": 1,
            "start": 50,
            "end": 150,
            "state": 0
        }
        self.create_region(bad_data, assert_status=status.HTTP_400_BAD_REQUEST)

    def test_get_region_by_machine_name(self):
        '''
        Get region details by machine name...
        '''
        region = get_region_by_machine_name('utr1')
        self.assertTrue(
            region is not None,
            'Could not look up region %s using '
            'the get_region_by_machine_name utility.')

    def test_get_bad_pool_name(self):
        '''
        Makes sure an HTTP 404 is returned for a bad pool name.
        '''
        url = reverse('allocate-numbers', args=['fffff', '10'])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND, 'The framework returned the '
                         'wrong error code for a bad pool name- should be 404.')

    def test_no_region_found(self):
        '''
        Deactivate the test region and try to make a request from a pool
        with no regions that are active.
        '''
        data = {
            "machine_name": "utr1",
            "active": False,
        }
        self.modify_region(data)
        url = reverse('allocate-numbers', args=['utpool1', '10'])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND, 'The framework returned the '
                         'wrong error code for a bad pool name- should be 404.')

    def test_modify_region(self):
        '''
        Change the name of the test region...
        '''
        data = {"readable_name": "Unit Test Region One Changed", }
        self.modify_region(data)

    def test_delete_retion(self):
        '''
        Try to delete the test region.
        '''
        self.delete_region(None, assert_status=status.HTTP_204_NO_CONTENT)

    def test_delete_pool(self):
        '''
        Create the pool then delete it...
        '''
        url = reverse('pool-modify', args=['utpool1'])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_204_NO_CONTENT, 'The framework returned the '
                         'wrong error code for a bad pool name- should be 204.')

    def test_machine_name_validator(self):
        '''
        Try to create a pool with a bad machine name.
        '''
        data = {
            "readable_name": "created by validator unit test",
            "machine_name": "utp_ool1",
            "active": "true",
            "request_threshold": 100
        }
        self.create_pool(data, status.HTTP_400_BAD_REQUEST)
