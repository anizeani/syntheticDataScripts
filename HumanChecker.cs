using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.XR.WSA;

public class AABB
{
    public Vector2 Min { get; set; }
    public Vector2 Max { get; set; }

    public Vector2 Center => (Min + Max) / 2;
    private Vector2 ScreenSize => new Vector2(Screen.width, Screen.height);

    public string Tag { get; set; }
    public override string ToString()
    {
        Vector2 normalizedMin = Min / ScreenSize;
        Vector2 normalizedMax = Max / ScreenSize;
        normalizedMin = new Vector2(Mathf.Clamp01(normalizedMin.x), Mathf.Clamp01(normalizedMin.y));
        normalizedMax = new Vector2(Mathf.Clamp01(normalizedMax.x), Mathf.Clamp01(normalizedMax.y));

        var normalizedCenter = (normalizedMax + normalizedMin) / 2;
        var boxSize = (normalizedMax - normalizedMin);

        return $"0 {normalizedCenter.x} {normalizedCenter.y} {boxSize.x} {boxSize.y}";
    }
}
public static class AABBExtentions
{
    public static AABB GetAABB(this SkinnedMeshRenderer renderer)
    {
        Vector3[] pts = new Vector3[8];
        Bounds b = renderer.bounds;
        Camera cam = Camera.main;
        pts[0] = cam.WorldToScreenPoint(new Vector3(b.center.x + b.extents.x, b.center.y + b.extents.y, b.center.z + b.extents.z));
        pts[1] = cam.WorldToScreenPoint(new Vector3(b.center.x + b.extents.x, b.center.y + b.extents.y, b.center.z - b.extents.z));
        pts[2] = cam.WorldToScreenPoint(new Vector3(b.center.x + b.extents.x, b.center.y - b.extents.y, b.center.z + b.extents.z));
        pts[3] = cam.WorldToScreenPoint(new Vector3(b.center.x + b.extents.x, b.center.y - b.extents.y, b.center.z - b.extents.z));
        pts[4] = cam.WorldToScreenPoint(new Vector3(b.center.x - b.extents.x, b.center.y + b.extents.y, b.center.z + b.extents.z));
        pts[5] = cam.WorldToScreenPoint(new Vector3(b.center.x - b.extents.x, b.center.y + b.extents.y, b.center.z - b.extents.z));
        pts[6] = cam.WorldToScreenPoint(new Vector3(b.center.x - b.extents.x, b.center.y - b.extents.y, b.center.z + b.extents.z));
        pts[7] = cam.WorldToScreenPoint(new Vector3(b.center.x - b.extents.x, b.center.y - b.extents.y, b.center.z - b.extents.z));

        //Get them in GUI space
        for (int i = 0; i < pts.Length; i++) pts[i].y = Screen.height - pts[i].y;

        //Calculate the min and max positions
        Vector3 min = pts[0];
        Vector3 max = pts[0];
        for (int i = 1; i < pts.Length; i++)
        {
            min = Vector3.Min(min, pts[i]);
            max = Vector3.Max(max, pts[i]);
        }

        return new AABB { Min=min, Max=max, Tag = renderer.tag };
    }
}

public class HumanChecker : MonoBehaviour
{
    SkinnedMeshRenderer[] mRenderer;
    SkinnedMeshRenderer[] wRenderer;
    GameObject[] men;
    GameObject[] women;
    public float margin = 0;
    public Rect boundingBox = new Rect();

    Bounds b = new Bounds();
    private Vector3[] pts = new Vector3[8];

    float time = 5.0f;

    private void Start()
    {
        StartCoroutine(ExecuteAfterSeconds(2));
    }

    IEnumerator ExecuteAfterSeconds(int seconds)
    {
        yield return new WaitForSeconds(seconds);
        men = GameObject.FindGameObjectsWithTag("0");
        women = GameObject.FindGameObjectsWithTag("1");
        mRenderer = new SkinnedMeshRenderer[men.Length];
        wRenderer = new SkinnedMeshRenderer[women.Length];
        GameObject.FindGameObjectsWithTag("0")
            .Select(go=> go.GetComponent<SkinnedMeshRenderer>())
            .Where(r => IsVisible(r))
            .Select(r => r.GetAABB())
            .ToArray();
        GameObject.FindGameObjectsWithTag("1")
            .Select(go => go.GetComponent<SkinnedMeshRenderer>())
            .Where(r => IsVisible(r))
            .Select(r => r.GetAABB())
            .ToArray();
    }

    void Update()
    {
        if(time >= 0)
        {
            time -= Time.deltaTime;
        }
        else
        {
            OutputVisibleRenderers(men);
            OutputVisibleRenderers(women);
        }

    }

    void OutputVisibleRenderers(GameObject[] humans)
    {
        foreach (var human in humans)
        {
            SkinnedMeshRenderer renderer = human.GetComponent<SkinnedMeshRenderer>();
            b = renderer.bounds;

            // output only the visible renderers' name
            if (IsVisible(renderer))
            {
                boundingBox.height = renderer.bounds.size.y; 
                boundingBox.width = renderer.bounds.size.x;
                boundingBox.center = renderer.bounds.center;
                Camera cam = Camera.main;

                //The object is behind us
                if (cam.WorldToScreenPoint(b.center).z < 0) continue;

                //All 8 vertices of the bounds
                pts[0] = cam.WorldToScreenPoint(new Vector3(b.center.x + b.extents.x, b.center.y + b.extents.y, b.center.z + b.extents.z));
                pts[1] = cam.WorldToScreenPoint(new Vector3(b.center.x + b.extents.x, b.center.y + b.extents.y, b.center.z - b.extents.z));
                pts[2] = cam.WorldToScreenPoint(new Vector3(b.center.x + b.extents.x, b.center.y - b.extents.y, b.center.z + b.extents.z));
                pts[3] = cam.WorldToScreenPoint(new Vector3(b.center.x + b.extents.x, b.center.y - b.extents.y, b.center.z - b.extents.z));
                pts[4] = cam.WorldToScreenPoint(new Vector3(b.center.x - b.extents.x, b.center.y + b.extents.y, b.center.z + b.extents.z));
                pts[5] = cam.WorldToScreenPoint(new Vector3(b.center.x - b.extents.x, b.center.y + b.extents.y, b.center.z - b.extents.z));
                pts[6] = cam.WorldToScreenPoint(new Vector3(b.center.x - b.extents.x, b.center.y - b.extents.y, b.center.z + b.extents.z));
                pts[7] = cam.WorldToScreenPoint(new Vector3(b.center.x - b.extents.x, b.center.y - b.extents.y, b.center.z - b.extents.z));

                //Get them in GUI space
                for (int i = 0; i < pts.Length; i++) pts[i].y = Screen.height - pts[i].y;

                //Calculate the min and max positions
                Vector3 min = pts[0];
                Vector3 max = pts[0];
                for (int i = 1; i < pts.Length; i++)
                {
                    min = Vector3.Min(min, pts[i]);
                    max = Vector3.Max(max, pts[i]);
                }

                //Construct a rect of the min and max positions and apply some margin
                boundingBox = Rect.MinMaxRect(min.x, min.y, max.x, max.y);
                boundingBox.xMin -= margin;
                boundingBox.xMax += margin;
                boundingBox.yMin -= margin;
                boundingBox.yMax += margin;
            }
        }
    }

    private void OnGUI()
    {
        Vector2 min = Camera.main.WorldToScreenPoint(b.min);
        Vector2 max = Camera.main.WorldToScreenPoint(b.max);
        GUI.Box(Rect.MinMaxRect(min.x,min.y,max.x,max.y), "");
    }

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
}
