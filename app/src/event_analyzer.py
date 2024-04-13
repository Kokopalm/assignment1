class EventAnalyzer:
    @staticmethod
    def get_joiners_multiple_meetings(events):
        joiners_dict = {}
        for event in events:
            joiners = event.get('joiners', [])
            for joiner in joiners:
                if joiner in joiners_dict:
                    joiners_dict[joiner] += 1
                else:
                    joiners_dict[joiner] = 1
        
        joiners_multiple_meetings = [joiner for joiner, count in joiners_dict.items() if count >= 2]
        return joiners_multiple_meetings

