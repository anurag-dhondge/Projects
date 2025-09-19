package com.marvellous.MarvellousPortal.Entity;

import lombok.*;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.core.mapping.Document;

@Document (collection = "BatchDetails")
//@Getter
//@Setter
//@NoArgsConstructor
//@AllArgsConstructor
@Data//replace above all

public class BatchEntry
{
    private ObjectId id;
    private String name;
    private int fees;
}
