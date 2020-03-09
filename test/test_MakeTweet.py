import pprint

from src.__main__ import MakeTweet


class TestGetTweetText:

    '''
    cancel_info = {
        対象日・時限,
        科目,
        教員,
        開講所属,
        休講理由
    }
    '''

    # 日本語
    def test_correct_1(self):
        cancel_info = {
            'period':             '2020年1月9日(木)  1限',
            'course_name':        'ドイツ語 IIb【Aクラス】*',
            'instructor':         'ドイツ文学科教員',
            'course_affiliation': 'ドイツ文学科',
            'cancel_reason':      '(F)  その他'
        }
        ret_val = self.fetch_tweet_text(cancel_info)
        correct_val =\
            '2020年1月9日(木)  1限\n'\
            '科目: ドイツ語 IIb【Aクラス】*\n'\
            '教員: ドイツ文学科教員\n'\
            '開講所属: ドイツ文学科\n'\
            '理由: (F)  その他'

        assert ret_val == correct_val

    # 英語
    def test_correct_2(self):
        cancel_info = {
            'period':             '2020年1月9日(木)  2限',
            'course_name':        'ACADEMIC SKILLS 1*',
            'instructor':         'DUPLICE John',
            'course_affiliation': '言語教育研究センター',
            'cancel_reason':      '(B)  学会'
        }
        ret_val = self.fetch_tweet_text(cancel_info)
        correct_val =\
            '2020年1月9日(木)  2限\n'\
            '科目: ACADEMIC SKILLS 1*\n'\
            '教員: DUPLICE John\n'\
            '開講所属: 言語教育研究センター\n'\
            '理由: (B)  学会'

        assert ret_val == correct_val

    # 複数教員
    def test_correct_3(self):
        cancel_info = {
            'period':             '2020年1月10日(金)  2限',
            'course_name':        'ドイツ語総合４（中級）*',
            'instructor':         '岩﨑/HAVRANEK',
            'course_affiliation': '言語教育研究センター',
            'cancel_reason':      '(C)  病気'
        }
        ret_val = self.fetch_tweet_text(cancel_info)
        correct_val =\
            '2020年1月10日(金)  2限\n'\
            '科目: ドイツ語総合４（中級）*\n'\
            '教員: 岩﨑/HAVRANEK\n'\
            '開講所属: 言語教育研究センター\n'\
            '理由: (C)  病気'

        assert ret_val == correct_val

    def fetch_tweet_text(self, cancel_info):
        make_tweet = MakeTweet({})
        tweet_text = make_tweet.get_tweet_text(cancel_info)
        return tweet_text


class TestCreateTweetList:

    def test_correct_1(self):
        cancel_info_table = [
            # tweet-1
            {
                'period': '2020年1月9日(木)  1限',
                'course_name': 'ドイツ語 IIb【Aクラス】*',
                'instructor': 'ドイツ文学科教員',
                'course_affiliation': 'ドイツ文学科',
                'cancel_reason': '(F)  その他'
            },
            # tweet-2
            {
                'period':             '2020年1月9日(木)  2限',
                'course_name':        'ACADEMIC SKILLS 1*',
                'instructor':         'DUPLICE John',
                'course_affiliation': '言語教育研究センター',
                'cancel_reason':      '(B)  学会'
            },
            # tweet-3
            {
                'period':             '2020年1月10日(金)  2限',
                'course_name':        'ドイツ語総合４（中級）*',
                'instructor':         '岩﨑/HAVRANEK',
                'course_affiliation': '言語教育研究センター',
                'cancel_reason':      '(C)  病気'
            }
        ]
        ret_val = self.fetch_tweet_list(cancel_info_table)
        correct_val = [
            # tweet-1
            ('2020年1月9日(木)  1限\n'
             '科目: ドイツ語 IIb【Aクラス】*\n'
             '教員: ドイツ文学科教員\n'
             '開講所属: ドイツ文学科\n'
             '理由: (F)  その他'),
            # tweet-2
            ('2020年1月9日(木)  2限\n'
             '科目: ACADEMIC SKILLS 1*\n'
             '教員: DUPLICE John\n'
             '開講所属: 言語教育研究センター\n'
             '理由: (B)  学会'),
            # tweet-3
            ('2020年1月10日(金)  2限\n'
             '科目: ドイツ語総合４（中級）*\n'
             '教員: 岩﨑/HAVRANEK\n'
             '開講所属: 言語教育研究センター\n'
             '理由: (C)  病気')
        ]

    def fetch_tweet_list(self, cancel_info_table):
        make_tweet = MakeTweet(cancel_info_table)
        tweet_list = make_tweet.create_tweet_list()
        return tweet_list
