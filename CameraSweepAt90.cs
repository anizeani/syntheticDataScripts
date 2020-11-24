using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;

public class CameraSweepAt90 : MonoBehaviour
{
    private int _height;

    const int TOTAL_IMAGES = 900;
    const float TEST_IMAGE_PERCENT = .2f;
    List<GameObject> humans;

    int testNum;
    int imageNum = 1;
    int maxNormalImageNumber;
    string parentPath;

    string testLabelPath;
    string trainLabelPath;

    string testImagePath;
    string testImageWithMaterialColor;
    string testImagePathImages;
    string testPathAnnotations;

    string trainImagePath;
    string trainImageWithMaterialColor;
    string trainImagePathImages;
    string trainPathAnnotations;
    GameObject[] men;
    GameObject[] women;
    int incrementX = 30;
    public int incrementZ = 100;

    int updateCounter = 0;
    int takeImageCounter = 0;

    Vector3 terrainSize;
    Terrain terrain;
    int xBound = 100;
    int zBound = 100;
    //probably should forloop over different height, starting at 3m going up to 100m
    public int height { get => _height; set => _height = value; }
    bool secondApproachWithFancyMaterial = false;

    // Start is called before the first frame update
    void Start()
    {
        humans = new List<GameObject>();

        //Folder Initialization
        CreateDirectories();
        CreateLabelFiles();
        CreateLabelMap();
        testNum = Mathf.RoundToInt(TOTAL_IMAGES * TEST_IMAGE_PERCENT);

        // get terrain to later know it's boarders
        terrain = GameObject.Find("Terrain").GetComponent<Terrain>();
        terrainSize = terrain.terrainData.size;

        transform.eulerAngles = new Vector3(90, 0, 90);
        transform.position = new Vector3(xBound, 200, zBound);
        Vector3 p = new Vector3(xBound, terrain.SampleHeight(transform.position) + height, zBound);
        transform.position = p;
    }

    // Update is called once per frame
    void Update()
    {
        Debug.Log(this.height);
        updateCounter++;
        if (updateCounter == 1) return;
        if (transform.position.x < terrainSize.x - xBound)
        {
            transform.position = new Vector3(transform.position.x + incrementX, terrain.SampleHeight(transform.position + Vector3.right * incrementX) + height, transform.position.z);
            // take picture
        }
        else if (transform.position.z < terrainSize.z - zBound)
        {
            transform.position = new Vector3(xBound, terrain.SampleHeight(transform.position) + height, transform.position.z + incrementZ);
        }
        else if (secondApproachWithFancyMaterial == false)
        {
            secondApproachWithFancyMaterial = true;
            maxNormalImageNumber = imageNum;
            imageNum = 1;
            //try this after: 
            transform.position = new Vector3(xBound, 200, zBound);
            transform.position = new Vector3(xBound + incrementX, terrain.SampleHeight(transform.position + Vector3.right * incrementX) + height, zBound);
            Material unlitColoredMaterial = (Material)Resources.Load("unlitForSecondSweep", typeof(Material));
            men = GameObject.FindGameObjectsWithTag("man");
            women = GameObject.FindGameObjectsWithTag("woman");
            unlitColoredMaterial.SetColor("_Color", Color.red);
            men
                .SelectMany(go => go.GetComponentsInChildren<SkinnedMeshRenderer>())
                .ToList()
                .ForEach(r =>
                {
                    r.material = unlitColoredMaterial;
                    //r.material.SetColor("_Color", Color.red);
                }
                );
            women
                .SelectMany(go => go.GetComponentsInChildren<SkinnedMeshRenderer>())
                .ToList()
                .ForEach(r =>
                {
                    r.material = unlitColoredMaterial;
                }
                );
        }
        else if (height < 100)
        {
            height += 5;
            foreach (GameObject man in men) Destroy(man);
            foreach (GameObject woman in women) Destroy(woman);
            Destroy(GameObject.Find("HumanGenerator").GetComponent<GenerateHumansAtRandomPosition>());
            GameObject.Find("HumanGenerator").AddComponent<GenerateHumansAtRandomPosition>();
            Destroy(Camera.main.gameObject.GetComponent<DelayCameraSweep>());
            Destroy(Camera.main.gameObject.GetComponent<CameraSweepAt90>());
            var delayCamera = Camera.main.gameObject.AddComponent<DelayCameraSweep>();
            delayCamera.height = this.height;
        }
        else UnityEditor.EditorApplication.isPlaying = false;
        StartCoroutine(TakePictures());
    }

    public void changeHeight(int additionalHeight)
    {
        this.height += additionalHeight;
    }

    private IEnumerator TakePictures()
    {
        yield return new WaitForEndOfFrame();
        TakeFullScreenPicture();
        //var name = GetFilename();
        //Debug.Log("Writing screenshot: " + name);
        //ScreenCapture.CaptureScreenshot(name);
    }

    void TakeFullScreenPicture()
    {
        if (imageNum == maxNormalImageNumber)
            return;
        takeImageCounter++;
        //Texture2D photo = new Texture2D(Screen.width, Screen.height, TextureFormat.RGB24, false);
        //photo.ReadPixels(new Rect(0, 0, Screen.width, Screen.height), 0, 0, false);
        //photo.Apply();
        //byte[] data = photo.EncodeToJPG(100);
        //DestroyImmediate(photo);
        if (imageNum > testNum)
        {
            //bb = boundingBox
            if (secondApproachWithFancyMaterial == false)
            {
                ScreenCapture.CaptureScreenshot(trainImagePath + "/images/" + imageNum + "_CaptureScreenshotFunction" + height + ".jpg", 4);
                //File.WriteAllBytes(trainImagePath + "/images/" + imageNum + "_" + height + ".jpg", data);
                var men = FindAllVisibleHumans("0");
                var women = FindAllVisibleHumans("1");
                var allBbs = men.Concat(women);
                File.WriteAllText(
                    trainImagePath + "/annotations/" + imageNum + "_" + height + ".txt",
                    string.Join(
                        System.Environment.NewLine,
                        allBbs
                        .Select(bb =>
                        {

                            //File.WriteAllText(trainImagePath + "/" + imageNum + "_getCoordinates.txt",$"{bb.Center} {bb.Min} {bb.Max}");
                            return bb.ToString();
                        }
                        )));
                //File.WriteAllText(trainImagePath + "/" + imageNum + "_position.txt",
                //    transform.position.ToString());
            }
            else
            {
                ScreenCapture.CaptureScreenshot(trainImagePath + "/colored/" + imageNum + "_CaptureScreenshotFunction_pink" + height + ".jpg", 4);
                //File.WriteAllBytes(trainImagePath + "/colored/" + imageNum + "_" + height + "_pink.jpg", data);
                //File.WriteAllText(trainImagePath + "/" + imageNum + "_pink_position.txt",
                //    transform.position.ToString());
            }
        }
        else
        {
            if (secondApproachWithFancyMaterial == false)
            {
                ScreenCapture.CaptureScreenshot(testImagePath + "/images/" + imageNum + "_CaptureScreenshotFunction" + height + ".jpg", 4);
                //File.WriteAllBytes(testImagePath + "/images/" + imageNum + "_" + height + ".jpg", data);
                var men = FindAllVisibleHumans("0");
                var women = FindAllVisibleHumans("1");
                var allBbs = men.Concat(women);
                File.WriteAllText(
                    testImagePath + "/annotations/" + imageNum + "_" + height + ".txt",
                    string.Join(
                        System.Environment.NewLine,
                        allBbs.Select(bb => bb.ToString())));
                //File.WriteAllText(testImagePath + "/" + imageNum + "_position.txt",
                //    transform.position.ToString());
            }
            else
            {
                ScreenCapture.CaptureScreenshot(testImagePath + "/colored/" + imageNum + "CaptureScreenshotFunction_pink" + height + ".jpg", 4);
                //File.WriteAllBytes(testImagePath + "/colored/" + imageNum + "_" + height + "_pink.jpg", data);
                //File.WriteAllText(testImagePath + "/" + imageNum + "_pink_position.txt",
                //    transform.position.ToString());
            }

        }

        if (imageNum == TOTAL_IMAGES)
        {
            UnityEditor.EditorApplication.isPlaying = false;
            Debug.Log("Training data collected!");
        }
        else
        {
            imageNum++;
        }
    }

    AABB[] FindAllVisibleHumans(string tag)
    {
        var human = GameObject.FindGameObjectsWithTag(tag)
            .Select(go => go.GetComponent<SkinnedMeshRenderer>())
            .Where(r => IsVisible(r))
            .Select(r => r.GetAABB())
            .ToArray();
        return human;
    }

    void CreateDirectories()
    {
        //create parent folder
        parentPath = "C:\\Users\\eventura\\Documents\\MLdataset";
        CreateDirectoryFromPathName(parentPath);
        //if (!File.Exists(parentPath))
        //{
        //    Directory.CreateDirectory(parentPath);
        //}
        //create test and train folders
        //testImagePath = parentPath + "/test";
        testImagePath = parentPath + "\\test";
        DeleteDirectoriesAndFilesInDirectories(testImagePath);
        CreateDirectoryFromPathName(testImagePath);
        //if (!File.Exists(testImagePath))
        //{
        //    Directory.CreateDirectory(testImagePath);
        //}
        //testImageWithMaterialColor = parentPath + "/test/colored";
        testImageWithMaterialColor = parentPath + "\\test\\colored";
        CreateDirectoryFromPathName(testImageWithMaterialColor);
        //if (!File.Exists(testImageWithMaterialColor))
        //{
        //    Directory.CreateDirectory(testImageWithMaterialColor);
        //}
        //testImagePathImages = parentPath + "/test/images";
        testImagePathImages = parentPath + "\\test\\images";
        CreateDirectoryFromPathName(testImagePathImages);
        //if (!File.Exists(testImagePathImages))
        //{
        //    Directory.CreateDirectory(testImagePathImages);
        //}
        //testPathAnnotations = parentPath + "/test/annotations";
        testPathAnnotations = parentPath + "\\test\\annotations";
        CreateDirectoryFromPathName(testPathAnnotations);
        //if (!File.Exists(testPathAnnotations))
        //{
        //    Directory.CreateDirectory(testPathAnnotations);
        //}
        //trainImagePath = parentPath + "/train";
        trainImagePath = parentPath + "\\train";
        DeleteDirectoriesAndFilesInDirectories(trainImagePath);
        CreateDirectoryFromPathName(trainImagePath);

        //trainImageWithMaterialColor = parentPath + "/train/colored";
        trainImageWithMaterialColor = parentPath + "\\train\\colored";
        CreateDirectoryFromPathName(trainImageWithMaterialColor);
        //if (!File.Exists(trainImageWithMaterialColor))
        //{
        //    Directory.CreateDirectory(trainImageWithMaterialColor);
        //}
        //trainImagePathImages = parentPath + "/train/images";
        trainImagePathImages = parentPath + "\\train\\images";
        CreateDirectoryFromPathName(trainImagePathImages);
        //if (!File.Exists(trainImagePathImages))
        //{
        //    Directory.CreateDirectory(trainImagePathImages);
        //}
        //trainPathAnnotations = parentPath + "/train/annotations";
        trainPathAnnotations = parentPath + "\\train\\annotations";
        CreateDirectoryFromPathName(trainPathAnnotations);
        //if (!File.Exists(trainPathAnnotations))
        //{
        //    Directory.CreateDirectory(trainPathAnnotations);
        //}
    }

    private void CreateDirectoryFromPathName(string path)
    {
        if (!File.Exists(path))
        {
            Directory.CreateDirectory(path);
        }
    }

    void CreateLabelFiles()
    {
        //create label files
        testLabelPath = parentPath + "/test.txt";
        File.WriteAllText(testLabelPath, "");
        trainLabelPath = parentPath + "/train.txt";
        File.WriteAllText(trainLabelPath, "");
    }

    void CreateLabelMap()
    {
        string labelMapPath = parentPath + "/labelmap.pbtxt";
        string labelMap = "";
        List<string> uniqueNames = new List<string>();
        GameObject humanGenerator = GameObject.Find("HumanGenerator");
        foreach (Transform child in humanGenerator.transform)
        {
            if (!uniqueNames.Contains(child.gameObject.name))
            {
                uniqueNames.Add(child.gameObject.name);
                labelMap += "item {\n" +
                "\tid: " + (child.GetSiblingIndex() + 1) + "\n" +
                "\tname: '" + child.gameObject.name.Replace("(Clone)", "") + "'\n" +
                "}\n";
            }
        }
        File.WriteAllText(labelMapPath, labelMap);
    }

    //void WriteObjectsToFile(Dictionary<GameObject, Rect> objects)
    //{
    //    //image_id, image_width, image_height, label_name, x1, x2, y1, y2 
    //    string line = imageNum + "," + Screen.width + "," + Screen.height;
    //    foreach (KeyValuePair<GameObject, Rect> obj in objects)
    //    {

    //        Rect tfRect = ConvertUnityRectToTensorflow(obj.Value);

    //        //make sure bounds are within image
    //        if (tfRect.xMin != tfRect.xMax && tfRect.yMin != tfRect.xMax)
    //        {
    //            line += "," + obj.Key.name + "," + tfRect.xMin + ","
    //                + tfRect.xMax + "," + tfRect.yMin + "," + tfRect.yMax;
    //        }
    //    }

    //    StreamWriter writer;

    //    if (imageNum > testNum)
    //    {
    //        writer = new StreamWriter(trainLabelPath, true);
    //    }
    //    else
    //    {
    //        writer = new StreamWriter(testLabelPath, true);
    //    }

    //    writer.WriteLine(line);
    //    writer.Close();
    //}
    //Rect ConvertUnityRectToTensorflow(Rect unityRect)
    //{
    //    return new Rect
    //    {
    //        xMin = Mathf.RoundToInt(unityRect.xMin),
    //        xMax = Mathf.RoundToInt(unityRect.xMax),
    //        yMin = Screen.height - Mathf.RoundToInt(unityRect.yMax),
    //        yMax = Screen.height - Mathf.RoundToInt(unityRect.yMin)
    //    };
    //}


    private bool IsVisible(Renderer renderer)
    {
        Plane[] planes = GeometryUtility.CalculateFrustumPlanes(Camera.main);

        if (GeometryUtility.TestPlanesAABB(planes, renderer.bounds))
        {
            //           Debug.Log(renderer.bounds.center);
            //           Debug.Log(renderer.bounds.size);

            return true;
        }
        else
            return false;
    }

    private void DeleteDirectoriesAndFilesInDirectories(string path)
    {
        System.IO.DirectoryInfo di = new DirectoryInfo(path);

        foreach (DirectoryInfo dir in di.EnumerateDirectories())
        {
            foreach (FileInfo file in dir.EnumerateFiles())
            {
                file.Delete();
            }
            dir.Delete(true);
        }
    }
}
