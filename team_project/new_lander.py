import random
import sys
import pygame

# ==========================================
# 1. ENVIRONMENT & PHYSICS (Simple Setup)
# ==========================================
lander = {"altitude": 100.0, "velocity": 0.0, "fuel": 50}
GRAVITY = -0.0057
THRUST_POWER = 0.012
SAFE_VELOCITY = -0.7


def reset_lander():
    lander["altitude"] = 100.0
    lander["velocity"] = 0.0
    lander["fuel"] = 150


def step_environment(action):
    # Action 1 = Thrust, Action 0 = Coast
    if action == 1 and lander["fuel"] > 0:
        acceleration = GRAVITY + THRUST_POWER
        lander["fuel"] -= 1
        thrusting = True
    else:
        acceleration = GRAVITY
        thrusting = False

    lander["velocity"] += acceleration
    lander["altitude"] += lander["velocity"]
    if lander["altitude"] < 0:
        lander["altitude"] = 0

    return thrusting


# ==========================================
# 2. Q-LEARNING AGENT (The Brain)
# ==========================================
q_table = {
    "High_Falling": {0: 0.0, 1: 0.0},
    "High_Raising": {0: 0.0, 1: 0.0},
    "Low_Falling":  {0: 0.0, 1: 0.0},
    "Low_Rising":   {0: 0.0, 1: 0.0},
    "On_grounding": {0: 0.0, 1: 0.0}
}


def get_state():
    if lander["altitude"] <= 0:
        return "On_grounding"
    is_high = lander["altitude"] > 50
    is_falling = lander["velocity"] < 0
    if is_high:
        return "High_Falling" if is_falling else "High_Raising"
    else:
        return "Low_Falling" if is_falling else "Low_Rising"


def choose_action(state, epsilon):
    if random.random() < epsilon:
        return random.choice([0, 1])
    return 1 if q_table[state][1] > q_table[state][0] else 0


# Train the agent before visualization starts
print("Training agent...")
epsilon = 0.9
for _ in range(2000):
    reset_lander()
    for _ in range(1000):
        s = get_state()
        a = choose_action(s, epsilon)
        step_environment(a)
        next_s = get_state()

        # Reward function
        # Inside the training loop:
        reward = -1
        if a == 1:
            reward = -2  # Penalize wasting fuel so it learns to coast more!

        if lander["velocity"] > 0:
            reward = -10

        if next_s == "On_grounding":
            reward = 100 if lander["velocity"] > SAFE_VELOCITY else -100

        q_table[s][a] += 0.1 * (
            reward + 0.9 * max(q_table[next_s].values()) - q_table[s][a]
        )
        if next_s == "On_grounding":
            break

        if next_s == "On_grounding":
            reward = 100 if lander["velocity"] > SAFE_VELOCITY else -100

        # Q-update equation
        q_table[s][a] += 0.1 * \
            (reward + 0.9 * max(q_table[next_s].values()) - q_table[s][a])
        if next_s == "On_grounding":
            break
    epsilon = max(0.01, epsilon * 0.995)
print("Training Complete!")

# ==========================================
# 3. REALISTIC VISUAL HELPERS
# ==========================================
pygame.init()
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lunar Lander Real-time Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas", 15)

# Pre-generate stars for smooth performance
stars = [(random.randint(0, WIDTH), random.randint(
    0, HEIGHT - 100), random.randint(1, 2)) for _ in range(70)]


def draw_apollo_lander(x, y, is_thrusting):
    """Draws a multi-stage Apollo-style lander."""
    # 1. Landing Gear / Legs
    pygame.draw.line(screen, (180, 180, 180),
                     (x - 12, y + 15), (x - 24, y + 32), 3)
    pygame.draw.line(screen, (180, 180, 180),
                     (x + 12, y + 15), (x + 24, y + 32), 3)
    pygame.draw.rect(screen, (100, 100, 100),
                     (x - 28, y + 30, 8, 3))  # Footpad Left
    pygame.draw.rect(screen, (100, 100, 100),
                     (x + 20, y + 30, 8, 3))  # Footpad Right

    # 2. Descent Stage (Gold Foil Base)
    pygame.draw.rect(screen, (212, 175, 55),
                     (x - 15, y, 30, 16), border_radius=2)

    # 3. Ascent Stage (Metallic Cabin Top)
    pygame.draw.polygon(screen, (200, 205, 215), [
                        (x - 12, y), (x + 12, y), (x + 8, y - 16), (x - 8, y - 16)])
    pygame.draw.circle(screen, (50, 150, 220), (x, y - 8), 5)  # Window

    # 4. Realistic Engine Exhaust Glow (Layered Transparent Surfaces)
    if is_thrusting:
        glow_surf = pygame.Surface((40, 50), pygame.SRCALPHA)
        # Outer plume (Soft Orange)
        pygame.draw.polygon(glow_surf, (255, 140, 0, 120),
                            [(12, 0), (28, 0), (20, 45)])
        # Inner core (Hot Yellow/White)
        pygame.draw.polygon(glow_surf, (255, 255, 200, 220), [
                            (16, 0), (24, 0), (20, 25)])
        screen.blit(glow_surf, (x - 20, y + 15))

# ==========================================
# 4. MAIN SIMULATION LOOP
# ==========================================


def run_simulation():
    reset_lander()
    running = True

    while running:
        clock.tick(60)  # 60 FPS

        # Handle inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_lander()

        # Step physics using trained model
        state = get_state()
        thrusting = False
        if state != "On_grounding":
            action = choose_action(state, epsilon=0)  # Pure exploitation
            thrusting = step_environment(action)

        # --- DRAWING ---
        screen.fill((8, 10, 20))  # Deep Space Blue

        # Draw Starfield
        for sx, sy, s_size in stars:
            pygame.draw.circle(screen, (200, 220, 255), (sx, sy), s_size)

        # Draw Lunar Surface & Touchdown Pad
        pygame.draw.rect(screen, (70, 75, 85),
                         (0, HEIGHT - 80, WIDTH, 80))  # Moon surface
        pygame.draw.ellipse(screen, (50, 55, 65),
                            (80, HEIGHT - 70, 120, 25))  # Crater
        pygame.draw.rect(screen, (0, 230, 120), (WIDTH//2 -
                         40, HEIGHT - 83, 80, 5))  # Green Pad

        # Convert Lander Altitude (0-100) to Screen Coordinates
        lander_x = WIDTH // 2
        lander_y = HEIGHT - 80 - 32 - int(lander["altitude"] * 5.2)

        # Draw Lander
        draw_apollo_lander(lander_x, lander_y, thrusting)

        # Draw HUD Telemetry Panel
        hud = font.render(
            f"Altitude : {lander['altitude']:6.1f} m", True, (255, 255, 255))
        vel_color = (100, 255, 100) if lander['velocity'] > SAFE_VELOCITY else (
            255, 100, 100)
        vel_hud = font.render(
            f"Velocity : {lander['velocity']:6.3f} m/s", True, vel_color)
        fuel_hud = font.render(
            f"Fuel     : {lander['fuel']:6d}", True, (255, 255, 255))

        screen.blit(hud, (20, 20))
        screen.blit(vel_hud, (20, 40))
        screen.blit(fuel_hud, (20, 60))

        # Status Overlay on Landing
        if state == "On_grounding":
            msg = "SUCCESSFUL TOUCHDOWN!" if lander["velocity"] > SAFE_VELOCITY else "CRASH LANDING!"
            color = (100, 255, 100) if lander["velocity"] > SAFE_VELOCITY else (
                255, 80, 80)
            lbl = font.render(msg, True, color)
            rst = font.render("Press 'R' to Restart", True, (200, 200, 200))
            screen.blit(lbl, (WIDTH//2 - lbl.get_width()//2, HEIGHT//2))
            screen.blit(rst, (WIDTH//2 - rst.get_width()//2, HEIGHT//2 + 25))

        pygame.display.flip()


if __name__ == "__main__":
    run_simulation()
