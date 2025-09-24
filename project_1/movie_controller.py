from database import Database
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
from typing import List, Dict, Optional
from datetime import datetime

# Consignes : 
# 1. Films sortis en 1999
# 2. Films dont le "genres" inclut "Comedy"
# 3. Films avec le "title" exacte "The Matrix"
# 4. Films avec un "runtime" supérieur a 120 minutes
# 5. Afficher seulment le "title" et "year" de tous les films
# 6. Films avec un "imdb.rating" supérieur à 8
# 7. Films sortis entre 1990 et 2000
# 8. Films dont le "genres" inclut "Sci-Fi" et "Action"
# 9. Films ou "Tom Hanks" est dans le "cast"
# 10. Films avec un "plot" contenant le mot "space"
# 11. Afficher les 10 films les mieux notés (imdb.rating), triés par note décroissante.
# 12. Afficher les 5 films les plus récents.
# 13. Afficher les films comédies (Comedy) avec le plus long runtime.
# 14. Compter le nombre total de films par genre.
# 15. Trouver la note moyenne IMDb (imdb.rating) par genre.
# 16. Lister les acteurs les plus fréquents dans la base.
# 17. Compter le nombre de commentaires (comments) par film.
# 18. Trouver le film avec le plus grand nombre de votes IMDb (imdb.votes).
# 19. Lister tous les films avec leurs commentaires (utiliser $lookup entre movies et comments).
# 20. Trouver tous les films avec au moins un commentaire posté après 2020.
# 21. Compter le nombre de commentaires par utilisateur.

class MovieController:
    """
    Reusable MongoDB controller for movie database operations.
    Implements comprehensive querying capabilities for the sample_mflix database.
    """
    
    def __init__(self, database: Database):
        """Initialize the MovieController with database connection."""
        self.client = database.client
        self.database = database.database
        self.movies = database.movies
        self.comments = database.comments
        self.users = database.users
    
    def close_connection(self):
        """Close the database connection."""
        self.client.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - automatically closes connection."""
        self.close_connection()
    
    # ===== BASIC FILTERING QUERIES =====
    
    def get_movies_by_year(self, year: int) -> List[Dict]:
        """1. Films sortis en 1999 (ou une année donnée)"""
        try:
            return list(self.movies.find({"year": year}))
        except Exception as e:
            print(f"Error fetching movies by year: {e}")
            return []
    
    def get_movies_by_genre(self, genre: str) -> List[Dict]:
        """2. Films dont le 'genre' inclut 'Comedy' (ou un genre donné)"""
        try:
            return list(self.movies.find({"genres": genre}))
        except Exception as e:
            print(f"Error fetching movies by genre: {e}")
            return []
    
    def get_movie_by_exact_title(self, title: str) -> Optional[Dict]:
        """3. Films avec le 'title' exacte 'The Matrix' (ou un titre donné)"""
        try:
            return self.movies.find_one({"title": title})
        except Exception as e:
            print(f"Error fetching movie by title: {e}")
            return None
    
    def get_movies_by_runtime(self, min_runtime: int) -> List[Dict]:
        """4. Films avec un 'runtime' supérieur à 120 minutes (ou une durée donnée)"""
        try:
            return list(self.movies.find({"runtime": {"$gt": min_runtime}}))
        except Exception as e:
            print(f"Error fetching movies by runtime: {e}")
            return []
    
    def get_movies_title_and_year(self) -> List[Dict]:
        """5. Afficher seulement le 'title' et 'year' de tous les films"""
        try:
            return list(self.movies.find({}, {"title": 1, "year": 1, "_id": 0}))
        except Exception as e:
            print(f"Error fetching movies title and year: {e}")
            return []
    
    def get_movies_by_rating(self, min_rating: float) -> List[Dict]:
        """6. Films avec un 'imdb.rating' supérieur à 8 (ou une note donnée)"""
        try:
            return list(self.movies.find({"imdb.rating": {"$gt": min_rating}}))
        except Exception as e:
            print(f"Error fetching movies by rating: {e}")
            return []
    
    def get_movies_by_year_range(self, start_year: int, end_year: int) -> List[Dict]:
        """7. Films sortis entre 1990 et 2000 (ou une période donnée)"""
        try:
            return list(self.movies.find({
                "year": {"$gte": start_year, "$lte": end_year}
            }))
        except Exception as e:
            print(f"Error fetching movies by year range: {e}")
            return []
    
    def get_movies_by_multiple_genres(self, genres: List[str]) -> List[Dict]:
        """8. Films dont le 'genres' inclut 'Sci-Fi' et 'Action' (ou plusieurs genres)"""
        try:
            return list(self.movies.find({"genres": {"$all": genres}}))
        except Exception as e:
            print(f"Error fetching movies by multiple genres: {e}")
            return []
    
    def get_movies_by_cast_member(self, actor: str) -> List[Dict]:
        """9. Films où 'Tom Hanks' est dans le 'cast' (ou un acteur donné)"""
        try:
            return list(self.movies.find({"cast": actor}))
        except Exception as e:
            print(f"Error fetching movies by cast member: {e}")
            return []
    
    def get_movies_by_plot_keyword(self, keyword: str) -> List[Dict]:
        """10. Films avec un 'plot' contenant le mot 'space' (ou un mot-clé donné)"""
        try:
            return list(self.movies.find({
                "plot": {"$regex": keyword, "$options": "i"}
            }))
        except Exception as e:
            print(f"Error fetching movies by plot keyword: {e}")
            return []
    
    # ===== SORTING AND LIMITING QUERIES =====
    
    def get_top_rated_movies(self, limit: int = 10) -> List[Dict]:
        """11. Afficher les 10 films les mieux notés (imdb.rating), triés par note décroissante"""
        try:
            return list(self.movies.find(
                {"imdb.rating": {"$exists": True, "$ne": None, "$gte": 1}},
                {"title": 1, "year": 1, "imdb": 1, "_id": 0}
            ).sort("imdb.rating", -1).limit(limit))
        except Exception as e:
            print(f"Error fetching top rated movies: {e}")
            return []
    
    def get_most_recent_movies(self, limit: int = 5) -> List[Dict]:
        """12. Afficher les 5 films les plus récents"""
        try:
            return list(self.movies.find(
                {"year": {"$exists": True, "$ne": None}},
                {"title": 1, "year": 1, "_id": 0}
            ).sort("year", -1).limit(limit))
        except Exception as e:
            print(f"Error fetching most recent movies: {e}")
            return []
    
    def get_longest_comedy_movies(self, limit: int = 10) -> List[Dict]:
        """13. Afficher les films comédies (Comedy) avec le plus long runtime"""
        try:
            return list(self.movies.find(
                {
                    "genres": "Comedy",
                    "runtime": {"$exists": True, "$ne": None}
                },
                {"title": 1, "runtime": 1, "year": 1, "_id": 0}
            ).sort("runtime", -1).limit(limit))
        except Exception as e:
            print(f"Error fetching longest comedy movies: {e}")
            return []
    
    # ===== AGGREGATION QUERIES =====
    
    def count_movies_by_genre(self) -> List[Dict]:
        """14. Compter le nombre total de films par genre"""
        try:
            pipeline = [
                {"$unwind": "$genres"},
                {"$group": {
                    "_id": "$genres",
                    "count": {"$sum": 1}
                }},
                {"$sort": {"count": -1}}
            ]
            return list(self.movies.aggregate(pipeline))
        except Exception as e:
            print(f"Error counting movies by genre: {e}")
            return []
    
    def get_average_rating_by_genre(self) -> List[Dict]:
        """15. Trouver la note moyenne IMDb (imdb.rating) par genre"""
        try:
            pipeline = [
                {"$match": {"imdb.rating": {"$exists": True, "$ne": None}}},
                {"$unwind": "$genres"},
                {"$group": {
                    "_id": "$genres",
                    "average_rating": {"$avg": "$imdb.rating"},
                    "movie_count": {"$sum": 1}
                }},
                {"$sort": {"average_rating": -1}}
            ]
            return list(self.movies.aggregate(pipeline))
        except Exception as e:
            print(f"Error calculating average rating by genre: {e}")
            return []
    
    def get_most_frequent_actors(self, limit: int = 20) -> List[Dict]:
        """16. Lister les acteurs les plus fréquents dans la base"""
        try:
            pipeline = [
                {"$unwind": "$cast"},
                {"$group": {
                    "_id": "$cast",
                    "movie_count": {"$sum": 1}
                }},
                {"$sort": {"movie_count": -1}},
                {"$limit": limit}
            ]
            return list(self.movies.aggregate(pipeline))
        except Exception as e:
            print(f"Error fetching most frequent actors: {e}")
            return []
    
    def count_comments_per_movie(self) -> List[Dict]:
        """17. Compter le nombre de commentaires (comments) par film"""
        try:
            pipeline = [
                {"$group": {
                    "_id": "$movie_id",
                    "comment_count": {"$sum": 1}
                }},
                {"$lookup": {
                    "from": "movies",
                    "localField": "_id",
                    "foreignField": "_id",
                    "as": "movie_info"
                }},
                {"$unwind": "$movie_info"},
                {"$project": {
                    "movie_title": "$movie_info.title",
                    "comment_count": 1,
                    "_id": 1
                }},
                {"$sort": {"comment_count": -1}}
            ]
            return list(self.comments.aggregate(pipeline))
        except Exception as e:
            print(f"Error counting comments per movie: {e}")
            return []
    
    def get_movie_with_most_votes(self) -> Optional[Dict]:
        """18. Trouver le film avec le plus grand nombre de votes IMDb (imdb.votes)"""
        try:
            return self.movies.find_one(
                {"imdb.votes": {"$exists": True, "$ne": None, "$gte": 1}},
                {"title": 1, "year": 1, "imdb": 1, "_id": 0},
                sort=[("imdb.votes", -1)]
            )
        except Exception as e:
            print(f"Error fetching movie with most votes: {e}")
            return None
    
    # ===== LOOKUP QUERIES =====
    
    def get_movies_with_comments(self, limit: int = 10) -> List[Dict]:
        """19. Lister tous les films avec leurs commentaires (utiliser $lookup entre movies et comments)"""
        try:
            comment_counts = self.count_comments_per_movie()
            results = []
            
            for movie_data in comment_counts[:limit]:
                movie_id = movie_data.get('_id')
                
                movie_comments = list(self.comments.find(
                    {"movie_id": movie_id}, 
                    {"name": 1, "text": 1, "date": 1, "_id": 0}
                ))
                
                result = {
                    "title": movie_data.get('movie_title'),
                    "comment_count": movie_data.get('comment_count'),
                    "comments": movie_comments
                }
                results.append(result)
                
            return results
        except Exception as e:
            print(f"Error fetching movies with comments: {e}")
            return []
    
    def get_movies_with_recent_comments(self, year: int = 2012) -> List[Dict]:
        """20. Trouver tous les films avec au moins un commentaire posté après 2012"""
        try:
            pipeline = [
                {"$match": {"date": {"$gte": datetime(year, 1, 1, 0, 0, 0)}}},
                {"$group": {"_id": "$movie_id"}},
                {"$project": {"movie_id": "$_id", "_id": 0}}
            ]
            
            recent_comment_movies = list(self.comments.aggregate(pipeline))

            movie_ids = [doc["movie_id"] for doc in recent_comment_movies]
            
            return list(self.movies.find(
                {"_id": {"$in": movie_ids}},
                {"title": 1, "year": 1, "_id": 0}
            ))
        except Exception as e:
            print(f"Error fetching movies with recent comments: {e}")
            return []
    
    def count_comments_per_user(self) -> List[Dict]:
        """21. Compter le nombre de commentaires par utilisateur"""
        try:
            pipeline = [
                {"$group": {
                    "_id": "$name",
                    "comment_count": {"$sum": 1}
                }},
                {"$sort": {"comment_count": -1}}
            ]
            return list(self.comments.aggregate(pipeline))
        except Exception as e:
            print(f"Error counting comments per user: {e}")
            return []
