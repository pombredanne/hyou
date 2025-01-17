import unittest

import gdata.spreadsheets.client
import mox

import hyou.client


class FakeSpreadsheetFeed(object):
  def __init__(self, key):
    self._key = key

  def get_spreadsheet_key(self):
    return self._key


class FakeSpreadsheetsFeed(object):
  def __init__(self, entries):
    self.entry = entries


class CollectionTest(unittest.TestCase):
  def setUp(self):
    self.mox = mox.Mox()
    self.mox.StubOutClassWithMocks(hyou.client, 'Spreadsheet')
    self.client = self.mox.CreateMock(
        gdata.spreadsheets.client.SpreadsheetsClient)
    self.drive = self.mox.CreateMockAnything()
    self.collection = hyou.client.Collection(self.client, self.drive)

  def tearDown(self):
    self.mox.UnsetStubs()
    self.mox.VerifyAll()

  def test_accessors_with_constructor(self):
    banana_feed = FakeSpreadsheetFeed('banana')
    self.client.get_feed(
        hyou.client.SPREADSHEET_URL % 'banana',
        desired_class=gdata.spreadsheets.data.Spreadsheet
    ).AndReturn(banana_feed)
    banana = hyou.client.Spreadsheet(
        self.collection, self.client, self.drive, 'banana', banana_feed)
    self.mox.ReplayAll()

    # Indexing by a key
    self.assertEqual(banana, self.collection['banana'])

  def test_accessors_with_enumerator(self):
    apple_feed = FakeSpreadsheetFeed('apple')
    banana_feed = FakeSpreadsheetFeed('banana')
    cinamon_feed = FakeSpreadsheetFeed('cinamon')
    feed = FakeSpreadsheetsFeed([apple_feed, banana_feed, cinamon_feed])

    self.client.get_spreadsheets().AndReturn(feed)
    apple = hyou.client.Spreadsheet(
        self.collection, self.client, self.drive, 'apple', apple_feed)
    banana = hyou.client.Spreadsheet(
        self.collection, self.client, self.drive, 'banana', banana_feed)
    cinamon = hyou.client.Spreadsheet(
        self.collection, self.client, self.drive, 'cinamon', cinamon_feed)

    self.mox.ReplayAll()

    # iter()
    it = iter(self.collection)
    self.assertEqual('apple', it.next())
    self.assertEqual('banana', it.next())
    self.assertEqual('cinamon', it.next())
    self.assertRaises(StopIteration, it.next)
    # len()
    self.assertEqual(3, len(self.collection))
    # keys()
    self.assertEqual(['apple', 'banana', 'cinamon'], self.collection.keys())
    # values()
    self.assertEqual([apple, banana, cinamon], self.collection.values())
    # items()
    self.assertEqual(
        [('apple', apple), ('banana', banana), ('cinamon', cinamon)],
        self.collection.items())
    # Indexing by an integer
    self.assertEqual(apple, self.collection[0])
    self.assertEqual(banana, self.collection[1])
    self.assertEqual(cinamon, self.collection[2])
    # Indexing by a key
    self.assertEqual(apple, self.collection['apple'])
    self.assertEqual(banana, self.collection['banana'])
    self.assertEqual(cinamon, self.collection['cinamon'])

  def test_create_spreadsheet(self):
    files = self.mox.CreateMockAnything()
    self.drive.files().AndReturn(files)
    executor = self.mox.CreateMockAnything()
    files.insert(body={
        'title': 'Cinamon',
        'mimeType': 'application/vnd.google-apps.spreadsheet',
    }).AndReturn(executor)
    executor.execute().AndReturn({'id': 'cinamon'})

    cinamon_feed = FakeSpreadsheetFeed('cinamon')
    self.client.get_feed(
        hyou.client.SPREADSHEET_URL % 'cinamon',
        desired_class=gdata.spreadsheets.data.Spreadsheet
    ).AndReturn(cinamon_feed)
    cinamon = hyou.client.Spreadsheet(
        self.collection, self.client, self.drive, 'cinamon', cinamon_feed)

    worksheet = self.mox.CreateMockAnything()
    cinamon[0].AndReturn(worksheet)
    worksheet.set_size(2, 8)

    self.mox.ReplayAll()

    self.collection.create_spreadsheet('Cinamon', rows=2, cols=8)
