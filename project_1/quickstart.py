from movie_controller import MovieController
from database import Database


def main():
    """Demonstrate the MovieController usage following the exact order of consignes."""

    with MovieController(Database()) as controller:        
        
        print("1. Films sortis en 1999:")
        movies_1999 = controller.get_movies_by_year(1999)
        for movie in movies_1999[:3]:  # Show first 3
            print(f"  - {movie.get('title', 'N/A')} ({movie.get('year', 'N/A')})")
        print(f"   Total: {len(movies_1999)} movies\n")
        
        print("2. Films dont le 'genres' inclut 'Comedy':")
        comedies = controller.get_movies_by_genre("Comedy")
        for movie in comedies[:3]:
            print(f"  - {movie.get('title', 'N/A')} ({movie.get('year', 'N/A')})")
        print(f"   Total: {len(comedies)} comedy movies\n")
        
        print("3. Films avec le 'title' exacte 'The Matrix':")
        matrix = controller.get_movie_by_exact_title("The Matrix")
        if matrix:
            print(f"  - {matrix.get('title')} ({matrix.get('year')}) - Rating: {matrix.get('imdb', {}).get('rating', 'N/A')}")
        else:
            print("  - Not found")
        print()

        print("4. Films avec un 'runtime' supérieur à 120 minutes:")
        long_movies = controller.get_movies_by_runtime(120)
        for movie in long_movies[:3]:
            print(f"  - {movie.get('title')} ({movie.get('year')}) - Runtime: {movie.get('runtime')} min")
        print(f"   Total: {len(long_movies)} movies\n")

        print("5. Afficher seulement le 'title' et 'year' de tous les films:")
        movies_title_and_year = controller.get_movies_title_and_year()
        for movie in movies_title_and_year[:5]:  # Show first 5
            print(f"  - {movie.get('title')} ({movie.get('year')})")
        print(f"   Total: {len(movies_title_and_year)} movies\n")

        print("6. Films avec un 'imdb.rating' supérieur à 8:")
        high_rated_movies = controller.get_movies_by_rating(8)
        for movie in high_rated_movies[:3]:
            print(f"  - {movie.get('title')} ({movie.get('year')}) - Rating: {movie.get('imdb', {}).get('rating', 'N/A')}")
        print(f"   Total: {len(high_rated_movies)} movies\n")
        
        print("7. Films sortis entre 1990 et 2000:")
        movies_between_1990_and_2000 = controller.get_movies_by_year_range(1990, 2000)
        for movie in movies_between_1990_and_2000[:3]:
            print(f"  - {movie.get('title')} ({movie.get('year')})")
        print(f"   Total: {len(movies_between_1990_and_2000)} movies\n")
        
        print("8. Films dont le 'genres' inclut 'Sci-Fi' et 'Action':")
        sci_fi_action_movies = controller.get_movies_by_multiple_genres(["Sci-Fi", "Action"])
        for movie in sci_fi_action_movies[:3]:
            print(f"  - {movie.get('title')} ({movie.get('year')}) - Genres: {movie.get('genres')}")
        print(f"   Total: {len(sci_fi_action_movies)} movies\n")

        print("9. Films où 'Tom Hanks' est dans le 'cast':")
        tom_hanks_movies = controller.get_movies_by_cast_member("Tom Hanks")
        for movie in tom_hanks_movies[:3]:
            print(f"  - {movie.get('title')} ({movie.get('year')})")
            if movie.get('cast'):
                print(f"    Cast: {', '.join(movie.get('cast', [])[:4])}...")
        print(f"   Total: {len(tom_hanks_movies)} movies\n")
        
        print("10. Films avec un 'plot' contenant le mot 'space':")
        space_movies = controller.get_movies_by_plot_keyword("space")
        for movie in space_movies[:3]:
            plot = movie.get('plot', '')
            plot_preview = plot[:100] + "..." if len(plot) > 100 else plot
            print(f"  - {movie.get('title')} ({movie.get('year')})")
            print(f"    Plot: {plot_preview}")
        print(f"   Total: {len(space_movies)} movies\n")
        
        print("11. Les 10 films les mieux notés:")
        top_movies = controller.get_top_rated_movies(10)
        for movie in top_movies:
            rating = movie.get('imdb', {}).get('rating', 'N/A')
            print(f"  - {movie.get('title')} ({movie.get('year')}) - Rating: {rating}")
        print()
        
        print("12. Les 5 films les plus récents:")
        recent_movies = controller.get_most_recent_movies(5)
        for movie in recent_movies:
            print(f"  - {movie.get('title')} ({movie.get('year')})")
        print()
        
        print("13. Films comédies avec le plus long runtime:")
        comedy_movies = controller.get_longest_comedy_movies(5)
        for movie in comedy_movies:
            print(f"  - {movie.get('title')} ({movie.get('year')}) - Runtime: {movie.get('runtime')} min")
        print()
        
        print("14. Nombre total de films par genre:")
        genre_counts = controller.count_movies_by_genre()
        for genre in genre_counts[:10]:  # Top 10 genres
            print(f"  - {genre['_id']}: {genre['count']} movies")
        print()
        
        print("15. Note moyenne IMDb par genre:")
        average_ratings = controller.get_average_rating_by_genre()
        for genre in average_ratings[:10]:  # Top 10 genres by rating
            print(f"  - {genre['_id']}: {genre['average_rating']:.2f} ({genre['movie_count']} movies)")
        print()
        
        print("16. Acteurs les plus fréquents:")
        frequent_actors = controller.get_most_frequent_actors(10)
        for actor in frequent_actors:
            print(f"  - {actor['_id']}: {actor['movie_count']} movies")
        print()

        print("17. Nombre de commentaires par film:")
        comments_by_movie = controller.count_comments_per_movie()
        for movie in comments_by_movie[:5]:  # Top 5 most commented
            print(f"  - {movie.get('movie_title')}: {movie.get('comment_count')} comments")
        print()

        print("18. Film avec le plus grand nombre de votes IMDb:")
        most_voted_movie = controller.get_movie_with_most_votes()
        if most_voted_movie:
            votes = most_voted_movie.get('imdb', {}).get('votes', 'N/A')
            print(f"  - {most_voted_movie.get('title')} ({most_voted_movie.get('year')}) - Votes: {votes}")
        else:
            print("  - Not found")
        print()
        
        print("19. Films avec leurs commentaires :")
        movies_with_comments = controller.get_movies_with_comments(5)
        for movie in movies_with_comments:
            print(f"  - {movie.get('title')} - {movie.get('comment_count')} comments")
            for comment in movie.get('comments', [])[:2]:  # Show first 2 comments
                comment_text = comment.get('text', '')[:80] + "..." if len(comment.get('text', '')) > 80 else comment.get('text', '')
                print(f"    * {comment.get('name', 'Anonymous')}: {comment_text}")
                
        print()
        
        print("20. Films avec commentaires postés après 2020:")
        recent_comments_movies = controller.get_movies_with_recent_comments(2012)
        for movie in recent_comments_movies[:5]:  # Show first 5
            print(f"  - {movie.get('title')} ({movie.get('year')})")
        print(f"   Total: {len(recent_comments_movies)} movies\n")
        
        print("21. Nombre de commentaires par utilisateur:")
        comments_per_user = controller.count_comments_per_user()
        for user in comments_per_user[:10]:  # Top 10 commenters
            print(f"  - {user['_id']}: {user['comment_count']} comments")
        print()


if __name__ == "__main__":
    main()
