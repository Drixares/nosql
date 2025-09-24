from database import Database
from datetime import datetime, timezone

class Seeder:
    def __init__(self, db_instance):
        self.db = db_instance

    def seed_all(self):
        """Populate all collections with test data"""
        print("Starting database seeding...")

        # Clear existing data
        self.clear_collections()

        # Seed in order due to dependencies
        users = self.seed_users()
        teams = self.seed_teams(users)
        projects = self.seed_projects(users, teams)

        print("Database seeding completed!")
        return {
            'users': users,
            'teams': teams,
            'projects': projects
        }

    def clear_collections(self):
        """Clear all collections"""
        collections = ['users', 'teams', 'projects']
        for collection in collections:
            self.db._get_collection(collection).delete_many({})
        print("Collections cleared")

    def seed_users(self):
        """Seed users collection"""
        print("Seeding users...")

        users_data = [
            {
                "name": "Alice Martin",
                "email": "alice@company.com",
                "role": "admin"
            },
            {
                "name": "Bob Dupont",
                "email": "bob@company.com",
                "role": "developer"
            },
            {
                "name": "Claire Durand",
                "email": "claire@company.com",
                "role": "designer"
            },
            {
                "name": "David Moreau",
                "email": "david@company.com",
                "role": "manager"
            },
            {
                "name": "Eva Bernard",
                "email": "eva@company.com",
                "role": "developer"
            },
            {
                "name": "Frank Leblanc",
                "email": "frank@company.com",
                "role": "tester"
            },
            {
                "name": "Grace Rousseau",
                "email": "grace@company.com",
                "role": "designer"
            },
            {
                "name": "Henri Dubois",
                "email": "henri@company.com",
                "role": "developer"
            }
        ]

        users = self.db.create_items("users", users_data, "seeder")
        print(f"Created {len(users)} users")
        return users

    def seed_teams(self, users):
        """Seed teams collection with user references"""
        print("Seeding teams...")

        # Group users by role for team assignment
        developers = [u for u in users if u['role'] == 'developer']
        designers = [u for u in users if u['role'] == 'designer']
        admin = [u for u in users if u['role'] == 'admin']
        manager = [u for u in users if u['role'] == 'manager']
        tester = [u for u in users if u['role'] == 'tester']

        teams_data = [
            {
                "name": "Frontend Team",
                "members": [developers[0]['pid'], designers[0]['pid'], designers[1]['pid']]
            },
            {
                "name": "Backend Team",
                "members": [developers[1]['pid'], developers[2]['pid'], admin[0]['pid']]
            },
            {
                "name": "QA Team",
                "members": [tester[0]['pid'], developers[0]['pid']]
            },
            {
                "name": "Management Team",
                "members": [manager[0]['pid'], admin[0]['pid']]
            },
            {
                "name": "Full Stack Team",
                "members": [developers[0]['pid'], developers[1]['pid'], designers[0]['pid'], tester[0]['pid']]
            }
        ]

        teams = self.db.create_items("teams", teams_data, "seeder")
        print(f"Created {len(teams)} teams")
        return teams

    def seed_projects(self, users, teams):
        """Seed projects collection with team and user references"""
        print("Seeding projects...")

        projects_data = [
            {
                "name": "E-commerce Platform",
                "teams": [teams[0]['pid'], teams[1]['pid']],
                "tags": ["urgent", "frontend", "backend", "web"],
                "budget": 50000,
                "deadline": datetime(2024, 12, 31, tzinfo=timezone.utc)
            },
            {
                "name": "Mobile App Development",
                "teams": [teams[4]['pid']],
                "tags": ["mobile", "react-native", "urgent"],
                "budget": 35000,
                "deadline": datetime(2024, 10, 15, tzinfo=timezone.utc)
            },
            {
                "name": "API Microservices",
                "teams": [teams[1]['pid']],
                "tags": ["backend", "microservices", "api"],
                "budget": 25000,
                "deadline": datetime(2024, 11, 30, tzinfo=timezone.utc)
            },
            {
                "name": "User Interface Redesign",
                "teams": [teams[0]['pid']],
                "tags": ["frontend", "ui", "design"],
                "budget": 15000,
                "deadline": datetime(2024, 9, 30, tzinfo=timezone.utc)
            },
            {
                "name": "Data Analytics Dashboard",
                "teams": [teams[1]['pid'], teams[4]['pid']],
                "tags": ["analytics", "dashboard", "data"],
                "budget": 40000,
                "deadline": datetime(2025, 1, 31, tzinfo=timezone.utc)
            },
            {
                "name": "Security Audit System",
                "teams": [teams[2]['pid'], teams[1]['pid']],
                "tags": ["security", "audit", "urgent"],
                "budget": 30000,
                "deadline": datetime(2024, 11, 15, tzinfo=timezone.utc)
            },
            {
                "name": "Customer Support Portal",
                "teams": [teams[0]['pid'], teams[2]['pid']],
                "tags": ["support", "portal", "customer"],
                "budget": 20000,
                "deadline": datetime(2024, 12, 15, tzinfo=timezone.utc)
            },
            {
                "name": "Internal Tools Suite",
                "teams": [teams[4]['pid']],
                "tags": ["internal", "tools", "productivity"],
                "budget": 18000,
                "deadline": datetime(2025, 2, 28, tzinfo=timezone.utc)
            }
        ]

        projects = self.db.create_items("projects", projects_data, "seeder")
        print(f"Created {len(projects)} projects")
        return projects

    def get_sample_data(self, table, count=3):
        """Get sample data from a table for testing"""
        return self.db.get_items(table, limit=count, fields=[])

    def print_summary(self):
        """Print a summary of seeded data"""
        print("\n=== SEEDING SUMMARY ===")

        # Users summary
        users_count = len(self.db.get_items("users", fields=None))
        users_by_role = {}
        all_users = self.db.get_items("users", fields=["role"])
        for user in all_users:
            role = user.get('role', 'unknown')
            users_by_role[role] = users_by_role.get(role, 0) + 1

        print(f"Users: {users_count} total")
        for role, count in users_by_role.items():
            print(f"  - {role}: {count}")

        # Teams summary
        teams_count = len(self.db.get_items("teams", fields=None))
        print(f"Teams: {teams_count} total")

        # Projects summary
        projects_count = len(self.db.get_items("projects", fields=None))
        projects_by_tag = {}
        all_projects = self.db.get_items("projects", fields=["tags"])
        for project in all_projects:
            for tag in project.get('tags', []):
                projects_by_tag[tag] = projects_by_tag.get(tag, 0) + 1

        print(f"Projects: {projects_count} total")
        print("Popular tags:")
        for tag, count in sorted(projects_by_tag.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  - {tag}: {count}")

if __name__ == "__main__":
    db = Database()

    if not db.test_connection():
        print("Failed to connect to database!")
        exit(1)

    # Create seeder and populate database
    seeder = Seeder(db)
    result = seeder.seed_all()

    print("RESULT USERS", seeder.get_sample_data("users", 3))
    print("RESULT TEAMS", seeder.get_sample_data("teams", 3))
    print("RESULT PROJECTS", seeder.get_sample_data("projects", 3))

    seeder.print_summary()

    print("\nSample data created successfully!")