from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime, timezone

class Database:
    def __init__(self, connection_string=None):
        if connection_string:
            self.client = MongoClient(connection_string,
                                    server_api=ServerApi('1'),
                                    tlsAllowInvalidCertificates=True)
        else:
            load_dotenv()
            uri = os.getenv("MONGO_URI")
            self.client = MongoClient(uri,
                                    server_api=ServerApi('1'),
                                    tlsAllowInvalidCertificates=True)

        self.db = self.client.get_database("project_2_db")

        print("DATABASE NAME", self.db.name)

    def _generate_metadata(self, created_by=None):
        """Generate automatic metadata fields"""
        metadata = {
            'pid': str(uuid.uuid4()),
            'created_at': datetime.now(timezone.utc),
            'updated_at': datetime.now(timezone.utc)
        }
        if created_by:
            metadata['created_by'] = created_by
        return metadata

    def _get_collection(self, table):
        """Get collection by table name"""
        return self.db[table]

    def _build_field_projection(self, fields):
        """Build MongoDB projection based on fields parameter"""
        if fields is None:
            return {'pid': 1, '_id': 0}  # Return only pid when fields=None
        elif isinstance(fields, list) and len(fields) == 0:
            return {'_id': 0}  # Return all fields when fields=[]
        elif isinstance(fields, list):
            projection = {'pid': 1, '_id': 0}
            for field in fields:
                projection[field] = 1
            return projection
        return {'_id': 0}

    # PARTIE 2 - CREATE FUNCTIONS
    def create_item(self, table, item, created_by=None):
        """Create a single item in the specified table"""
        collection = self._get_collection(table)

        # Add metadata
        item.update(self._generate_metadata(created_by))

        # Insert the item
        collection.insert_one(item)

        # Return the created item using aggregate
        pipeline = [
            {'$match': {'pid': item['pid']}},
            {'$project': {'_id': 0}}
        ]

        created_item = list(collection.aggregate(pipeline))
        return created_item[0] if created_item else None

    def create_items(self, table, items, created_by=None):
        """Create multiple items in the specified table"""
        collection = self._get_collection(table)

        # Add metadata to each item
        for item in items:
            item.update(self._generate_metadata(created_by))

        # Insert all items
        result = collection.insert_many(items)

        # Return created items using aggregate
        pids = [item['pid'] for item in items]
        pipeline = [
            {'$match': {'pid': {'$in': pids}}},
            {'$project': {'_id': 0}}
        ]

        return list(collection.aggregate(pipeline))

    # PARTIE 4 - UPDATE FUNCTIONS
    def update_item_by_pid(self, table, pid, item_data, updated_by=None):
        """Update a single item by PID"""
        collection = self._get_collection(table)

        # Prepare update data
        update_data = {
            'updated_at': datetime.now(timezone.utc),
            **item_data
        }
        if updated_by:
            update_data['updated_by'] = updated_by

        # Use aggregate pipeline for update
        pipeline = [
            {'$match': {'pid': pid}},
            {'$addFields': update_data},
            {'$merge': {'into': table, 'whenMatched': 'replace'}}
        ]

        list(collection.aggregate(pipeline))
        return self.get_item_by_pid(table, pid, fields=[])

    def update_item_by_attr(self, table, attributes, item_data, updated_by=None):
        """Update a single item by attributes"""
        collection = self._get_collection(table)

        # Prepare update data
        update_data = {
            'updated_at': datetime.now(timezone.utc),
            **item_data
        }
        if updated_by:
            update_data['updated_by'] = updated_by

        # Use aggregate pipeline for update
        pipeline = [
            {'$match': attributes},
            {'$limit': 1},
            {'$addFields': update_data},
            {'$merge': {'into': table, 'whenMatched': 'replace'}}
        ]

        list(collection.aggregate(pipeline))
        return self.get_item_by_attr(table, attributes, fields=[])

    def update_items_by_pids(self, table, pids, items_data, updated_by=None):
        """Update multiple items by PIDs"""
        collection = self._get_collection(table)

        # Prepare update data
        update_data = {
            'updated_at': datetime.now(timezone.utc),
            **items_data
        }
        if updated_by:
            update_data['updated_by'] = updated_by

        # Use aggregate pipeline for update
        pipeline = [
            {'$match': {'pid': {'$in': pids}}},
            {'$addFields': update_data},
            {'$merge': {'into': table, 'whenMatched': 'replace'}}
        ]

        list(collection.aggregate(pipeline))
        return self.get_items(table, {'pid': {'$in': pids}}, fields=[])

    def update_items_by_attr(self, table, attributes, items_data, updated_by=None):
        """Update multiple items by attributes"""
        collection = self._get_collection(table)

        # Get items to update first to get their PIDs
        items_to_update = self.get_items(table, attributes, fields=['pid'])
        if not items_to_update:
            return []

        pids = [item['pid'] for item in items_to_update]

        # Prepare update data
        update_data = {
            'updated_at': datetime.now(timezone.utc),
            **items_data
        }
        if updated_by:
            update_data['updated_by'] = updated_by

        # Use aggregate pipeline for update
        pipeline = [
            {'$match': attributes},
            {'$addFields': update_data},
            {'$merge': {'into': table, 'whenMatched': 'replace'}}
        ]

        list(collection.aggregate(pipeline))
        return self.get_items(table, {'pid': {'$in': pids}}, fields=[])

    # PARTIE 5 - GET SIMPLE FUNCTIONS
    def get_item_by_pid(self, table, pid, fields=None, pipeline=None):
        """Get a single item by PID"""
        collection = self._get_collection(table)

        # Default to returning all fields for basic get operations
        if fields is None:
            fields = []

        base_pipeline = [{'$match': {'pid': pid}}]

        # Add custom pipeline if provided
        if pipeline:
            base_pipeline.extend(pipeline)

        # Add field projection
        projection = self._build_field_projection(fields)
        base_pipeline.append({'$project': projection})

        result = list(collection.aggregate(base_pipeline))
        return result[0] if result else None

    def get_item_by_attr(self, table, attributes, fields=None, pipeline=None):
        """Get a single item by attributes"""
        collection = self._get_collection(table)

        # Default to returning all fields for basic get operations
        if fields is None:
            fields = []

        base_pipeline = [
            {'$match': attributes},
            {'$limit': 1}
        ]

        # Add custom pipeline if provided
        if pipeline:
            base_pipeline.extend(pipeline)

        # Add field projection
        projection = self._build_field_projection(fields)
        base_pipeline.append({'$project': projection})

        result = list(collection.aggregate(base_pipeline))
        return result[0] if result else None

    # PARTIE 6 - DELETE FUNCTIONS
    def delete_item_by_pid(self, table, pid):
        """Delete a single item by PID"""
        collection = self._get_collection(table)
        result = collection.delete_one({'pid': pid})
        return result.deleted_count > 0

    def delete_item_by_attr(self, table, attributes):
        """Delete a single item by attributes"""
        collection = self._get_collection(table)
        result = collection.delete_one(attributes)
        return result.deleted_count > 0

    def delete_items_by_pids(self, table, pids):
        """Delete multiple items by PIDs"""
        collection = self._get_collection(table)
        result = collection.delete_many({'pid': {'$in': pids}})
        return result.deleted_count

    def delete_items_by_attr(self, table, attributes):
        """Delete multiple items by attributes"""
        collection = self._get_collection(table)
        result = collection.delete_many(attributes)
        return result.deleted_count

    # PARTIE 7 - ARRAY FUNCTIONS
    def array_push_item_by_pid(self, table, pid, array_field, new_item, updated_by=None):
        """Add an item to an array field by PID"""
        collection = self._get_collection(table)

        update_data = {'updated_at': datetime.now(timezone.utc)}
        if updated_by:
            update_data['updated_by'] = updated_by

        pipeline = [
            {'$match': {'pid': pid}},
            {'$addFields': {
                array_field: {'$concatArrays': [f'${array_field}', [new_item]]},
                **update_data
            }},
            {'$merge': {'into': table, 'whenMatched': 'replace'}}
        ]

        list(collection.aggregate(pipeline))
        return self.get_item_by_pid(table, pid, fields=[])

    def array_push_item_by_attr(self, table, attributes, array_field, new_item, updated_by=None):
        """Add an item to an array field by attributes"""
        collection = self._get_collection(table)

        update_data = {'updated_at': datetime.now(timezone.utc)}
        if updated_by:
            update_data['updated_by'] = updated_by

        pipeline = [
            {'$match': attributes},
            {'$addFields': {
                array_field: {'$concatArrays': [f'${array_field}', [new_item]]},
                **update_data
            }},
            {'$merge': {'into': table, 'whenMatched': 'replace'}}
        ]

        list(collection.aggregate(pipeline))
        return self.get_items(table, attributes, fields=[])

    def array_pull_item_by_pid(self, table, pid, array_field, item_attr, updated_by=None):
        """Remove an item from an array field by PID"""
        collection = self._get_collection(table)

        update_data = {'updated_at': datetime.now(timezone.utc)}
        if updated_by:
            update_data['updated_by'] = updated_by

        pipeline = [
            {'$match': {'pid': pid}},
            {'$addFields': {
                array_field: {
                    '$filter': {
                        'input': f'${array_field}',
                        'cond': {'$ne': ['$$this', item_attr]}
                    }
                },
                **update_data
            }},
            {'$merge': {'into': table, 'whenMatched': 'replace'}}
        ]

        list(collection.aggregate(pipeline))
        return self.get_item_by_pid(table, pid, fields=[])

    def array_pull_item_by_attr(self, table, attributes, array_field, item_attr, updated_by=None):
        """Remove an item from an array field by attributes"""
        collection = self._get_collection(table)

        update_data = {'updated_at': datetime.now(timezone.utc)}
        if updated_by:
            update_data['updated_by'] = updated_by

        pipeline = [
            {'$match': attributes},
            {'$addFields': {
                array_field: {
                    '$filter': {
                        'input': f'${array_field}',
                        'cond': {'$ne': ['$$this', item_attr]}
                    }
                },
                **update_data
            }},
            {'$merge': {'into': table, 'whenMatched': 'replace'}}
        ]

        list(collection.aggregate(pipeline))
        return self.get_items(table, attributes, fields=[])

    # PARTIE 8 - ADVANCED GET FUNCTION
    def get_items(self, table, attributes=None, fields=None, sort=None, skip=0, limit=None, return_stats=False, pipeline=None):
        """Advanced get function with filtering, sorting, pagination, and stats"""
        collection = self._get_collection(table)

        # Build base pipeline
        base_pipeline = []

        # Add filtering
        if attributes:
            base_pipeline.append({'$match': attributes})

        # Add custom pipeline before sorting and pagination
        if pipeline:
            base_pipeline.extend(pipeline)

        # For stats, count total items before pagination
        total_items = 0
        if return_stats:
            count_pipeline = base_pipeline + [{'$count': 'total'}]
            count_result = list(collection.aggregate(count_pipeline))
            total_items = count_result[0]['total'] if count_result else 0

        # Add sorting
        if sort:
            base_pipeline.append({'$sort': sort})

        # Add pagination
        if skip > 0:
            base_pipeline.append({'$skip': skip})
        if limit:
            base_pipeline.append({'$limit': limit})

        # Add field projection (only if no custom pipeline provided)
        if not pipeline:
            projection = self._build_field_projection(fields)
            base_pipeline.append({'$project': projection})

        # Execute pipeline
        results = list(collection.aggregate(base_pipeline))

        # Return with or without stats
        if return_stats:
            stats = {
                'itemsCount': total_items,
                'pagesCount': (total_items + limit - 1) // limit if limit and limit > 0 else 1,
                'firstIndexReturned': skip,
                'lastIndexReturned': skip + len(results) - 1 if results else skip,
                'itemsReturned': len(results)
            }
            return {'items': results, 'stats': stats}

        return results

    # CONNECTION TEST FUNCTION
    def test_connection(self):
        """Test MongoDB connection"""
        try:
            self.client.server_info()
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False