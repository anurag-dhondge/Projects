package com.marvellous.MarvellousPortal.controller;

import com.marvellous.MarvellousPortal.Entity.BatchEntry;
import com.marvellous.MarvellousPortal.service.BatchEntryService;
import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@RequestMapping("/batches")
public class BatchEntryController
{
    @Autowired
    private BatchEntryService batchEntryService;

    @GetMapping
    public ResponseEntity<?> getAll()
    {
        List<BatchEntry> allData = batchEntryService.getAll();

        if((allData != null)&& !allData.isEmpty())
        {
            return new ResponseEntity<>(allData, HttpStatus.OK);
        }
        else
        {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }


    @PostMapping
    public ResponseEntity<BatchEntry> createEntry(@RequestBody BatchEntry myentry)
    {
        //batchEntryService.saveEntry(myentry);
        //return "Document inserted successfully";
        try
        {
            batchEntryService.saveEntry(myentry);
            return new ResponseEntity<BatchEntry>(myentry,HttpStatus.CREATED);
        }
        catch (Exception eobj)
        {
            return new ResponseEntity<BatchEntry>(HttpStatus.BAD_REQUEST);
        }

    }



    @GetMapping("/id/{myid}")
    public ResponseEntity<BatchEntry> getBatchEntryById(@PathVariable ObjectId myid)  //springboot doesnt give its variable hence
    {
        //return batchEntryService.findById(myid).orElse(null);
        Optional <BatchEntry> batchEntry = batchEntryService.findById(myid);
        if(batchEntry.isPresent())
        {
            return new ResponseEntity<BatchEntry>(batchEntry.get(),HttpStatus.OK);
        }
        else
        {
            return new ResponseEntity<BatchEntry>(HttpStatus.NOT_FOUND);
        }
    }


    @DeleteMapping("/id/{myid}")

    public ResponseEntity<?>deleteEntryById(@PathVariable ObjectId myid)
    {
        batchEntryService.deleteById(myid);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @PutMapping ("/id/{myid}")
    public BatchEntry updateEntryById(@PathVariable ObjectId myid, @RequestBody BatchEntry myentry)
    {
        return batchEntryService.updateById(myid,myentry);
    }
}
