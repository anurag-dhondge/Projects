package AnuragPackerUnpacker;

import java.io.*;

public class AnuragUnpacker
{
    private String PackName;

    public AnuragUnpacker(String A)
    {
        this.PackName = A;
    }

    public void UnpackingActivity()
    {
        try
        {
            System.out.println("--------------------------------------------------------------------------------------");
            System.out.println("------------------------Anurag Packer Unpacker------------------------------------");
            System.out.println("--------------------------------------------------------------------------------------");
            System.out.println("-------------------------UnPacking Activity-------------------------------------------");
            System.out.println("--------------------------------------------------------------------------------------");

            String Header = null;
            File fobjnew = null;            
            int FileSize = 0 , iRet = 0 , iCountFile = 0;

            File fobj = new File(PackName);

            // If Packed File is not Present
            if(!fobj.exists())
            {
                System.out.println("Unable to Access Packed File ");
                return ;
            }

            System.out.println("Packed File Successfully Opened ");

            FileInputStream fiobj = new FileInputStream(fobj);

            //Buffer to read header
            byte HeaderBuffer[] = new byte[100];

            //Scanned the packed file to extract the files from it
            while((iRet = fiobj.read(HeaderBuffer,0,100))!=-1)
            {            
                //Conver Byte Array to String
                Header = new String(HeaderBuffer);

                Header = Header.trim();

                //Tokenized the header in 2 parts
                String Tokens[] = Header.split(" ");

                fobjnew = new File(Tokens[0]);

                //Create new file to extract
                fobjnew.createNewFile();

                FileSize = Integer.parseInt(Tokens[1]);

                //Create new buffer to Store file data
                byte Buffer[] = new byte[FileSize];

                FileOutputStream foobj = new FileOutputStream(fobjnew);

                //Read the data from packed file
                fiobj.read(Buffer,0,FileSize);

                //Write the data into extracted file
                foobj.write(Buffer,0,FileSize);

                System.out.println("File Unpacked with name : "+Tokens[0]+" having Size "+FileSize);

                iCountFile++;

                foobj.close();

            } //End of while

            System.out.println("--------------------------------------------------------------------------------------");
            System.out.println("---------------------------- Stastical Report ----------------------------------------");
            System.out.println("--------------------------------------------------------------------------------------");

            System.out.println("Total Number of Files Unpaked : " + iCountFile);

            System.out.println("--------------------------------------------------------------------------------------");
            System.out.println("--------------------- Thank You For Using Our Application ----------------------------");
            System.out.println("--------------------------------------------------------------------------------------");


            fiobj.close();
        }

        catch(Exception eobj)
        {

        }

    }
}