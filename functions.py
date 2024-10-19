import chess.pgn
import csv
import os

def count_games_in_pgn(file_path):
    game_count = 0
    with open(file_path) as pgn_file:
        while True:
            game = chess.pgn.read_headers(pgn_file)
            if game is None:
                break  # End of file
            game_count += 1
    return game_count

def build_a_csv_game(game, csv_headers):
    data = []
    error_logs = []
    for header in csv_headers:
        if header not in game:
            if header == "Site":
                error_logs.append(['?', 'Site'])
            else:
                error_logs.append([game['Site'], header ])
            data.append('?')
        else:
            data.append(game[header])
    return data, error_logs

def iter_games(file_path, start_count, stop_count, csv_game_headers, csv_games, csv_games_error_logs):
    game_count = 0
    with open(file_path) as pgn_file:
        while game_count < stop_count:
            game = chess.pgn.read_headers(pgn_file)
            if game_count >= start_count:
                if game is None:
                    print('broken at game_count: ', game_count)
                    break
                else:
                    csv_game, error_logs = build_a_csv_game(game, csv_game_headers)
                    csv_games.append(csv_game)
                    if len(error_logs) != 0:
                        csv_games_error_logs.append(error_logs)
            game_count += 1

# def write_to_csv(file_name, csv_games):
#     with open(file_name, 'w', newline='') as csvFile:
#         csvWriter = csv.writer(csvFile)
#         for csv_game in csv_games:
#             csvWriter.writerow(csv_game)

def write_to_csv(file_name, csv_games):
    # The file_name already includes the full path
    full_path = file_name
    
    # Create the directory structure if it doesn't exist
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    # Write the CSV file
    with open(full_path, 'w', newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        for csv_game in csv_games:
            csvWriter.writerow(csv_game)

def generate_batch_ranges_and_files(total_games, batch_size):
    full_batches = total_games // batch_size
    remaining = total_games % batch_size
    
    ranges_and_files = []
    for i in range(full_batches):
        start = i * batch_size
        end = start + batch_size - 1
        file_name = f"games_{start}-{end}.csv"
        ranges_and_files.append(([start, end], file_name))
    
    if remaining > 0:
        start = full_batches * batch_size
        end = total_games - 1
        file_name = f"games_{start}-{end}.csv"
        ranges_and_files.append(([start, end], file_name))
    
    return ranges_and_files