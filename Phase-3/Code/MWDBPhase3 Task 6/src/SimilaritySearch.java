import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.awt.image.DataBufferByte;
import java.io.*;
import java.util.*;

import org.jcodec.api.FrameGrab;
import org.jcodec.common.model.ColorSpace;
import org.jcodec.common.model.Picture;
import org.jcodec.scale.ColorUtil;
import org.jcodec.scale.Transform;

/**
 * Created by sruthimaddineni on 11/20/16.
 */
public class SimilaritySearch {
    String queryTokens[];
    public void compute_video_similarity(String hashFile, String query, int n) {
        queryTokens = query.split(";");
        Map<String, List<Map.Entry<String, String>>> bucketMap = new HashMap<>();
        List<String> siftVectors = new ArrayList<>();
        Map<String, Map<String, List<String>>> hashMap = new HashMap<>();
        try {
            BufferedReader buffer = new BufferedReader(new InputStreamReader(new FileInputStream(hashFile)));
            String line = buffer.readLine();
            while ((line != null) && !line.isEmpty())   {
                line = line.replaceAll("\\{|\\}|<|>", "");
                String tokens[] = line.split(",");
                Map<String, List<String>> innerMap = hashMap.get(tokens[0]);
                if (innerMap == null || innerMap.isEmpty())   {
                    innerMap = new HashMap<>();
                    innerMap.put(tokens[1], new ArrayList<>(Arrays.asList(tokens[2])));
                }   else    {
                    List<String> items = innerMap.get(tokens[1]);
                    if (items == null)  {
                        items = new ArrayList<>();
                        items.add(tokens[2]);
                    }   else {
                        items.add(tokens[2]);
                    }
                    innerMap.put(tokens[1], items);
                }
                hashMap.put(tokens[0], innerMap);
                if (isInTheWindow(tokens[2]))   {
                    siftVectors.add(tokens[2]);
                    List<Map.Entry<String, String>> buckets = bucketMap.get(tokens[2]);
                    if (buckets == null)    {
                        buckets = new ArrayList<>();
                    }
                    buckets.add(new AbstractMap.SimpleEntry<>(tokens[0], tokens[1]));
                    bucketMap.put(tokens[2], buckets);
                }
                line = buffer.readLine();
            }
            buffer.close();
            
        } catch (Exception e) {
            System.out.println("Exception ");
            e.printStackTrace();
        }
        System.out.println("Hash Map built!");
        System.out.println("Number of sift vectors in the rectangular region " + siftVectors.size());
        Map<String, Integer> vectorSim = new HashMap<>();
        int totalCount = 0;
        Set<String> buckets = new HashSet<>();
        for (String sift : siftVectors) {
            for (Map.Entry<String, String> bucket : bucketMap.get(sift))   {
                buckets.add(bucket.getKey() + bucket.getValue());
                List<String> vectors = hashMap.get(bucket.getKey()).get(bucket.getValue());
                totalCount += vectors.size();
                for (String vector : vectors)   {
                    String strs[] = vector.split(";");
                    if (strs[0].equals(queryTokens[0]))    {
                        continue;
                    }
                    String key = strs[0] + ";" + strs[1];
                    int val = vectorSim.getOrDefault(key, 0);
                    vectorSim.put(key, val+1);
                }
            }
        }
        try {
            BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("Task6-output.txt")));
            writer.write("Total number of sift vectors in the region - " + String.valueOf(siftVectors.size())+ "\n");
            writer.write("Total number of sift vectors considered - " + String.valueOf(totalCount) + "\n");
            writer.write("Total number of unique sift vectors considered - " + String.valueOf(vectorSim.size()) + "\n");
            writer.write("Total number of bytes accessed in terms of number of buckets accessed - " + String.valueOf(buckets.size()) + "\n");
            writer.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        List<String> sortedVectors = sortBasedOnValue(vectorSim);
        visualizeResults(sortedVectors.subList(0, sortedVectors.size() >= n ? n : sortedVectors.size()));
    }
    
    boolean isInTheWindow(String sift) {
        String tokens[] = sift.split(";");
        String coordinates[] = queryTokens[2].split(",");
        String coordinates1[] = queryTokens[3].split(",");
        if (Double.parseDouble(coordinates[0]) <= Double.parseDouble(tokens[3])
            && Double.parseDouble(coordinates1[0]) >= Double.parseDouble(tokens[3])
            && Double.parseDouble(coordinates[1]) <= Double.parseDouble(tokens[4])
            && Double.parseDouble(coordinates1[1]) >= Double.parseDouble(tokens[4])) {
            return true;
        }
        return false;
    }
    
    List<String> sortBasedOnValue(Map<String, Integer> vectorSim)  {
        List<String> vectors = new ArrayList<>(vectorSim.keySet());
        Collections.sort(vectors, new Comparator() {
            @Override
            public int compare(Object o1, Object o2) {
                int r1 = vectorSim.get(o1);
                int r2 = vectorSim.get(o2);
                if (r2 < r1) {
                    return 1;
                }
                return 0;
            }
        });
        return vectors;
    }
    
    void visualizeResults(List<String> vectors)   {
        for (String vector : vectors) {
            String tokens[] = vector.split(",|;");
            try {
                Picture frame = FrameGrab.getFrameAtSec(new File(tokens[0]), Integer.parseInt(tokens[1]));
                if (frame.getColor() != ColorSpace.RGB) {
                    Transform transform = ColorUtil.getTransform(frame.getColor(), ColorSpace.RGB);
                    Picture rgb = Picture.createCropped(frame.getWidth(), frame.getHeight(), ColorSpace.RGB, frame.getCrop());
                    transform.transform(frame, rgb);
                    //new RgbToBgr().transform(rgb, rgb);
                    frame = rgb;
                }
                
                BufferedImage dst = new BufferedImage(frame.getCroppedWidth(), frame.getCroppedHeight(),
                                                      BufferedImage.TYPE_3BYTE_BGR);
                
                byte[] data = ((DataBufferByte) dst.getRaster().getDataBuffer()).getData();
                int[] srcData = frame.getPlaneData(0);
                for (int i = 0; i < data.length; i++) {
                    data[i] = (byte) srcData[i];
                }
                ImageIO.write(dst, "bmp", new File(tokens[0] + "_" + tokens[1] + ".bmp"));
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
    
    public static void main(String str[])   {
        SimilaritySearch s = new SimilaritySearch();
        s.compute_video_similarity(str[0].replaceAll("\"", ""), str[1].replaceAll("\"", ""), Integer.parseInt(str[2].replaceAll("\"", "")));
    }
}
