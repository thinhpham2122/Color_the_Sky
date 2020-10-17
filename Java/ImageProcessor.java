import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.Iterator;

public class ImageProcessor {
    private static String inPath;
    private static String outPath;

    public static void main(String[] args) {
        String a = "E:/Pics/Original";
        inPath = "E:/Tech/Projects/Color_the_Sky/raw_image/";
        outPath = "E:/Tech/Projects/Color_the_Sky/feature/";

        String[] list = fileList();
        massResize(list);
    }

    // ++++++++++++++++++++++++++++++++++ Methods ++++++++++++++++++++++++++++++++++
    public static BufferedImage resizeImage(BufferedImage originalImage, int targetWidth, int targetHeight) throws IOException {
        BufferedImage resizedImage = new BufferedImage(targetWidth, targetHeight, BufferedImage.TYPE_INT_RGB);
        Graphics2D graphics2D = resizedImage.createGraphics();
        graphics2D.drawImage(originalImage, 0, 0, targetWidth, targetHeight, null);
        graphics2D.dispose();
        return resizedImage;
    }

    public static void massResize(String[] list) {
        Iterator iterator = Arrays.stream(list).iterator();
        int counter = 0;
        try {
            while (iterator.hasNext()) {
                String temp = (String) iterator.next();
                File input = new File(inPath + temp);
                File output = new File(outPath + "id" + counter + ".jpeg");
                BufferedImage inputImage = ImageIO.read(input);
                BufferedImage resizedImage = resizeImage(inputImage, 512, 512);
                ImageIO.write(resizedImage, "jpeg", output);
                System.out.println(temp);
                counter++;
            }
        } catch (Exception e) {}

    }

    public static String[] fileList() {
        File folder = new File(inPath);
        String[] files = folder.list();
//        for (String file : files)
//        {
//            System.out.println(file);
//        }
        return files;
    }
    // ++++++++++++++++++++++++++++++++++ Methods - End ++++++++++++++++++++++++++++++++++
}