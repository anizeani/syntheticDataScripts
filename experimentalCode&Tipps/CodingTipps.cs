// #1: you want to Debug into the .Select or .Where LINQ statements, but they are just evaluated when needed (lazy), if you write .ToList()
// it will be evaluated immediately, other option: write an extension method to IEnumerable: you want to extent the Method .Debug
// you always have to give this and the object type you give in, the second argument is the function/action (action ~ void function)
// for example: var x = GameObject.FindGameObjectsWithTag("man").SelectMany(go => go.GetComponentsInChildren<SkinnedMeshRenderer>()).Debug() ----- Debug will recieve A skillMeshedRenderer

public static class DebugExtensions
{
    public static IEnumerable<T> Debug<T>(this IEnumerable<T> collection, Action<T> handler)
    {
        var list = collection.ToList();
        foreach (var element in list)
        {
            handler(element);
        }
        return list;
    }
}

//#2
// Get All SkinnedMeshRenderers and set their material color: 
            men
                .SelectMany(go => go.GetComponentsInChildren<SkinnedMeshRenderer>())
                .ToList()
                .ForEach(r => r.material.SetColor("magenta", Color.magenta));

// if you want to find all people and get there bounds 

        var human = GameObject.FindGameObjectsWithTag(tag)
            .Select(go => go.GetComponent<SkinnedMeshRenderer>())
            .Where(r => IsVisible(r))
            .Select(r => r.GetAABB())
            .ToArray();
        return human;

// Iterate through all GameObjects with certain "Tag", get from each the renderer, check if they are visible, if they are, return A class object of type AABB (which has properties about tag, center and boxsize for yoloformat)
AABB[] FindAllVisibleHumans(string tag)
    {
        var human = GameObject.FindGameObjectsWithTag(tag)
            .Select(go => go.GetComponent<SkinnedMeshRenderer>())
            .Where(r => IsVisible(r))
            .Select(r => r.GetAABB())
            .ToArray();
        return human;
    }
//The tricky part: Select returns an IEnumerable, so we can write a public static extension class with a public static extension method, that will get the bounds and center from the renderer and perform operations on them and return an AABB object

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

// of course, we need to first define the class AABB:
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

        return $"{Tag} {normalizedCenter.x} {normalizedCenter.y} {boxSize.x} {boxSize.y}";
    }
}

