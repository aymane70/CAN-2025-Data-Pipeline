# =============================================================================
# lambarki aymane 
# github.com/aymane70
# =============================================================================

import os
import sys
import csv
import random
from datetime import datetime, timedelta
from faker import Faker
import logging

# ====================== CREATE DIRECTORIES IMMEDIATELY ======================

os.makedirs('generated_tables', exist_ok=True)
os.makedirs('logs', exist_ok=True)



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/data_generation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

fake = Faker()
random.seed(42)


START_DATE = datetime(2025, 1, 12)
STADIUMS = [
    {"name": "Stade Mohammed V", "city": "Casablanca", "capacity": 67000},
    {"name": "Stade Prince Moulay Abdellah", "city": "Rabat", "capacity": 52000},
    {"name": "Stade de Marrakech", "city": "Marrakech", "capacity": 45000},
    {"name": "Stade Adrar", "city": "Agadir", "capacity": 45000},
    {"name": "Stade de Fès", "city": "Fès", "capacity": 42000},
    {"name": "Stade Ibn Batouta", "city": "Tanger", "capacity": 65000}
]

TEAMS = [
    "Morocco", "Senegal", "Egypt", "Nigeria", "Algeria", "Cameroon",
    "Ivory Coast", "Ghana", "Tunisia", "Mali", "Burkina Faso", "Guinea",
    "South Africa", "DR Congo", "Zambia", "Gabon", "Benin", "Tanzania",
    "Mauritania", "Angola", "Mozambique", "Zimbabwe", "Namibia", "Comoros"
]

GROUPS = {
    "A": ["Morocco", "DR Congo", "Zambia", "Tanzania", "Benin", "Comoros"],
    "B": ["Senegal", "Cameroon", "Guinea", "Mozambique"],
    "C": ["Egypt", "Ghana", "Angola", "Zimbabwe"],
    "D": ["Nigeria", "Ivory Coast", "Mali", "Namibia"],
    "E": ["Algeria", "Burkina Faso", "Mauritania", "South Africa"],
    "F": ["Tunisia", "Gabon", "Guinea", "Morocco"]
}

POSITIONS = ["Goalkeeper", "Defender", "Midfielder", "Forward"]

def generate_teams():
    logger.info("Generating teams data...")
    filepath = os.path.join('generated_tables', 'teams.csv')
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['team_id', 'team_name', 'group_name', 'fifa_ranking', 'coach_name', 'coach_nationality'])
        
        for idx, team in enumerate(TEAMS, 1):
            group = [g for g, teams in GROUPS.items() if team in teams][0]
            ranking = random.randint(10, 120)
            coach = fake.name()
            coach_nat = random.choice(TEAMS)
            writer.writerow([idx, team, group, ranking, coach, coach_nat])
    logger.info(f"✓ teams.csv created at {filepath}")

def generate_players():
    logger.info("Generating players data...")
    filepath = os.path.join('generated_tables', 'players.csv')
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['player_id', 'team_id', 'player_name', 'position', 'age', 'height_cm', 'club', 'market_value_millions'])
        
        player_id = 1
        for team_id in range(1, len(TEAMS) + 1):
            for _ in range(23):
                name = fake.name()
                position = random.choice(POSITIONS)
                age = random.randint(19, 35)
                height = random.randint(165, 198)
                club = fake.company()
                value = round(random.uniform(0.5, 80), 1)
                writer.writerow([player_id, team_id, name, position, age, height, club, value])
                player_id += 1
    logger.info(f"✓ players.csv created with {player_id-1} players")

def generate_stadiums():
    logger.info("Generating stadiums data...")
    filepath = os.path.join('generated_tables', 'stadiums.csv')
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['stadium_id', 'stadium_name', 'city', 'capacity'])
        
        for idx, stadium in enumerate(STADIUMS, 1):
            writer.writerow([idx, stadium['name'], stadium['city'], stadium['capacity']])
    logger.info(f"✓ stadiums.csv created")

def generate_matches():
    logger.info("Generating matches data...")
    filepath = os.path.join('generated_tables', 'matches.csv')
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['match_id', 'match_date', 'stadium_id', 'home_team_id', 'away_team_id', 
                        'home_score', 'away_score', 'attendance', 'round', 'status'])
        
        match_id = 1
        current_date = START_DATE
        
        
        for group, teams in GROUPS.items():
            team_ids = [TEAMS.index(t) + 1 for t in teams]
            for i in range(len(team_ids)):
                for j in range(i + 1, len(team_ids)):
                    stadium_id = random.randint(1, len(STADIUMS))
                    home_score = random.randint(0, 4)
                    away_score = random.randint(0, 4)
                    attendance = random.randint(15000, STADIUMS[stadium_id-1]['capacity'])
                    
                    writer.writerow([match_id, current_date.strftime('%Y-%m-%d'), stadium_id,
                                   team_ids[i], team_ids[j], home_score, away_score,
                                   attendance, f"Group {group}", "Completed"])
                    match_id += 1
                    current_date += timedelta(days=random.randint(1, 2))
        
        
        rounds = ["Round of 16", "Quarter-finals", "Semi-finals", "Third Place", "Final"]
        matches_per_round = [8, 4, 2, 1, 1]
        
        for round_name, num_matches in zip(rounds, matches_per_round):
            for _ in range(num_matches):
                stadium_id = random.randint(1, len(STADIUMS))
                team1 = random.randint(1, len(TEAMS))
                team2 = random.randint(1, len(TEAMS))
                while team2 == team1:
                    team2 = random.randint(1, len(TEAMS))
                
                home_score = random.randint(0, 3)
                away_score = random.randint(0, 3)
                attendance = random.randint(30000, STADIUMS[stadium_id-1]['capacity'])
                
                writer.writerow([match_id, current_date.strftime('%Y-%m-%d'), stadium_id,
                               team1, team2, home_score, away_score,
                               attendance, round_name, "Completed"])
                match_id += 1
                current_date += timedelta(days=random.randint(2, 4))
    
    logger.info(f"✓ matches.csv created with {match_id-1} matches")
    return match_id - 1

def generate_match_events(total_matches):
    logger.info("Generating match events data...")
    filepath = os.path.join('generated_tables', 'match_events.csv')
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['event_id', 'match_id', 'player_id', 'event_type', 'minute', 'team_id'])
        
        event_id = 1
        
        with open(os.path.join('generated_tables', 'matches.csv'), 'r') as mf:
            matches = list(csv.DictReader(mf))
        
        for match in matches:
            match_id = int(match['match_id'])
            home_team = int(match['home_team_id'])
            away_team = int(match['away_team_id'])
            home_score = int(match['home_score'])
            away_score = int(match['away_score'])
            
            events = []
            
            
            for _ in range(home_score):
                player_id = (home_team - 1) * 23 + random.randint(1, 23)
                minute = random.randint(1, 90)
                events.append([event_id, match_id, player_id, "Goal", minute, home_team])
                event_id += 1
            
            for _ in range(away_score):
                player_id = (away_team - 1) * 23 + random.randint(1, 23)
                minute = random.randint(1, 90)
                events.append([event_id, match_id, player_id, "Goal", minute, away_team])
                event_id += 1
            
            
            for _ in range(random.randint(1, 5)):
                team = random.choice([home_team, away_team])
                player_id = (team - 1) * 23 + random.randint(1, 23)
                minute = random.randint(1, 90)
                events.append([event_id, match_id, player_id, "Yellow Card", minute, team])
                event_id += 1
            
            
            if random.random() < 0.15:
                team = random.choice([home_team, away_team])
                player_id = (team - 1) * 23 + random.randint(1, 23)
                minute = random.randint(1, 90)
                events.append([event_id, match_id, player_id, "Red Card", minute, team])
                event_id += 1
            
            writer.writerows(events)
    
    logger.info(f"✓ match_events.csv created with {event_id-1} events")

def generate_ticket_sales():
    logger.info("Generating ticket sales data...")
    filepath = os.path.join('generated_tables', 'ticket_sales.csv')
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['sale_id', 'match_id', 'sale_date', 'ticket_category', 'quantity', 'price_usd', 'total_revenue'])
        
        with open(os.path.join('generated_tables', 'matches.csv'), 'r') as mf:
            matches = list(csv.DictReader(mf))
        
        sale_id = 1
        for match in matches:
            match_id = int(match['match_id'])
            match_date = datetime.strptime(match['match_date'], '%Y-%m-%d')
            
            categories = [
                ("VIP", random.randint(50, 200), random.randint(150, 400)),
                ("Premium", random.randint(200, 800), random.randint(80, 150)),
                ("Standard", random.randint(1000, 3000), random.randint(30, 80)),
                ("Economy", random.randint(2000, 5000), random.randint(15, 30))
            ]
            
            for category, qty, price in categories:
                sale_date = match_date - timedelta(days=random.randint(1, 30))
                total = qty * price
                writer.writerow([sale_id, match_id, sale_date.strftime('%Y-%m-%d'), 
                               category, qty, price, total])
                sale_id += 1
    
    logger.info(f"✓ ticket_sales.csv created with {sale_id-1} records")

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Starting CAN 2025 Data Generation")
    logger.info("=" * 60)
    
    try:
        generate_teams()
        generate_players()
        generate_stadiums()
        total_matches = generate_matches()
        generate_match_events(total_matches)
        generate_ticket_sales()
        
        logger.info("=" * 60)
        logger.info("✓ All CSV files generated successfully!")
        logger.info("Files saved to: generated_tables/")
        logger.info("=" * 60)
        
        
        print("\n" + "="*60)
        print("DATA GENERATION COMPLETE!")
        print("="*60)
        print("Generated files in 'generated_tables/' directory:")
        for file in os.listdir('generated_tables'):
            filepath = os.path.join('generated_tables', file)
            size = os.path.getsize(filepath)
            print(f"  • {file} ({size:,} bytes)")
        
        print(f"\nLogs saved to: logs/data_generation.log")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Error during data generation: {str(e)}", exc_info=True)
        print(f"\n❌ Error: {str(e)}")
        print("Check logs/data_generation.log for details")
        sys.exit(1)