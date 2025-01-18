from functools import reduce

def _remap_by_queue_type(acc: dict, item: dict) -> dict:
    queue_type = item.get('queueType')
    acc[queue_type] = item
    return acc

def rank_data_by_queue_type(rank_data: list) -> dict:
    return reduce(_remap_by_queue_type, rank_data, {})


def _format_data(queue_data: dict) -> str:
    return f"{queue_data.get('tier')} {queue_data.get('rank')} {queue_data.get('leaguePoints')} LP Wins: {queue_data.get('wins')}, Losses: {queue_data.get('losses')}"

def display_ranked_data(username: str, tag: str, ranked_data: dict) -> str:
    player_rank_flex = _format_data(ranked_data.get('RANKED_FLEX_SR')) if ranked_data.get('RANKED_FLEX_SR') else "Not played yet..."
    player_rank_solo_duo = _format_data(ranked_data.get('RANKED_SOLO_5x5')) if ranked_data.get('RANKED_SOLO_5x5') else "Not played yet..."

    return [
            f'RiotID: {username}#{tag}',
            f'Solo/Duo Ranked: {player_rank_solo_duo}',
            f'Flex Ranked: {player_rank_flex}',
            ]
