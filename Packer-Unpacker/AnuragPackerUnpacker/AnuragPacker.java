package AnuragPackerUnpacker;

import java.io.*;

public class AnuragPacker
{
    private String PackName;
    private String DirName;
    
    public AnuragPacker(String A , String B)
    {
        this.PackName = A;
        this.DirName = B;
    }

    public void PackingActivity()
    {
        try
        {
            System.out.println("--------------------------------------------------------------------------------------");
            System.out.println("------------------------Anurag Packer Unpacker------------------------------------");
            System.out.println("--------------------------------------------------------------------------------------");
            System.out.println("---------------------------Packing Activity-------------------------------------------");
            System.out.println("--------------------------------------------------------------------------------------");
            
            int i = 0 , j = 0 , iRet = 0 , iCountFile = 0;

            File PackObj = new File(PackName);

            File fobj = new File(DirName);

            //Check The Existence Of Directory
            if((fobj.exists()) && (fobj.isDirectory())) //Check Directory(Folder)
            {
                System.out.println(DirName + " is Successfully Opened");

                //Create Packed File
                boolean bRet = PackObj.createNewFile();

                if(bRet == false)
                {
                    System.out.println("Unable to create pack file");
                    return;
                }

                System.out.println("Packed File Gets Successfully Created with : "+PackName);

                // Retrive All Files from Directory
                File Arr[] = fobj.listFiles();

                //Packed File Object
                FileOutputStream foobj = new FileOutputStream(PackObj);

                //Buffer for Read & Write Activity
                byte Buffer[] = new byte[1024]; 
                
                String Header = null;

                for(i = 0 ; i < Arr.length ; i++)     // Directory Traversal
                {
                    Header = Arr[i].getName() + " " +Arr[i].length();

                    //Loop to form 100 Byte Header
                    for(j= Header.length() ; j < 100 ; j++)
                    {
                        Header = Header + " ";
                    }

                    //Write Header into Packed File
                    foobj.write(Header.getBytes());     //String to byte

                    //Open File From Directory for Reading
                    FileInputStream fiobj = new FileInputStream((Arr[i]));

                    //Write Contents of File into Packed File
                    while((iRet = fiobj.read(Buffer))!= -1)
                    {
                        foobj.write(Buffer,0,iRet);
                        System.out.println("File Named Scaned : " + Arr[i].getName());
                        System.out.println("File Size Read is : " + iRet);
                    }

                    fiobj.close();








                    iCountFile++;

                }
                System.out.println("Packing Activity Done");
                System.out.println("--------------------------------------------------------------------------------------");
                System.out.println("---------------------------- Stastical Report ----------------------------------------");
                System.out.println("--------------------------------------------------------------------------------------");

                //To Be Add
                System.out.println("Total Files Packed : "+iCountFile);

                System.out.println("--------------------------------------------------------------------------------------");
                System.out.println("--------------------- Thank You For Using Our Application ----------------------------");
                System.out.println("--------------------------------------------------------------------------------------");

            }
            
            else
            {
                System.out.println("Directory is not present in current directory");
                return;
            }


        }   // End of try

        catch(Exception eobj)
        {

        }
    }   //End of PackingActivity Function
}   // End Of AnuragPacker class


//C:\Users\91989\Desktop\LB\PackerUnpacker>javac AnuragPacker.java -d .
