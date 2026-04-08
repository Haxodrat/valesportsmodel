# backend/tests/test_elo.py

from services.predictions import get_upcoming_predictions

def main():
    matches = get_upcoming_predictions()
    for m in matches[:10]:
        print(
            f"{m['teams'][0]} vs {m['teams'][1]} | "
            f"{m['team1_win_prob']:.2%} - {m['team2_win_prob']:.2%} | "
            f"winner: {m['predicted_winner']}"
        )

if __name__ == "__main__":
    main()