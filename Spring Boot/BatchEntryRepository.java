package com.marvellous.MarvellousPortal.Repository;

import com.marvellous.MarvellousPortal.Entity.BatchEntry;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.repository.MongoRepository;

// import
public interface BatchEntryRepository extends MongoRepository<BatchEntry, ObjectId>
{

}
