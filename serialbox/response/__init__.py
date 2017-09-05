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


def Response(RFResponse):
    '''
    An HTTP response that has additional fields defined for SerialBox list
    data.
    '''

    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None,
                 list=None):
        self.list = list or []
        super(Response, self).__init__(self, data=None, status=None,
                                       template_name=None, headers=None,
                                       exception=False, content_type=None)
