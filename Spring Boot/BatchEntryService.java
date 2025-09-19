package com.marvellous.MarvellousPortal.service;

import com.marvellous.MarvellousPortal.Entity.BatchEntry;
import com.marvellous.MarvellousPortal.Repository.BatchEntryRepository;
import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Optional;

@Component
public class BatchEntryService
{
    @Autowired
    private BatchEntryRepository batchEntryRepository;

    //C : Create
    //POST : http verb
    public void saveEntry(BatchEntry batchEntry)
    {
        batchEntryRepository.save(batchEntry);
    }

    //R : Read
    //GET : http verb
    public List<BatchEntry> getAll()
    {
        return batchEntryRepository.findAll();
    }
    public Optional<BatchEntry> findById(ObjectId id)
    {
        return batchEntryRepository.findById(id);
    }

    //D : Delete
    //DELETE : http verb
    public void deleteById(ObjectId id)
    {
        batchEntryRepository.deleteById(id);
    }

    //U : Update
    //PUT
    public BatchEntry updateById(ObjectId id, BatchEntry updated)
    {
        updated.setId(id);
        return batchEntryRepository.save(updated);

    }


}
