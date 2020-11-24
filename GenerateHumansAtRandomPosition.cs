using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GenerateHumansAtRandomPosition : MonoBehaviour
{
    private GameObject[] humans = new GameObject[2];
    private GameObject human;
    public int numberOfHumans = 200;
    public int height = 500;
    Vector3 realposi = new Vector3(0,0,0);
    // Start is called before the first frame update
    void Start()
    {
        GameObject man = Resources.Load("man") as GameObject;
        man = Instantiate(man, transform.position + Vector3.up, Quaternion.identity);
        GameObject woman = Resources.Load("woman") as GameObject;
        woman = Instantiate(woman, transform.position + Vector3.up, Quaternion.identity);
        humans[0] = man;
        humans[1] = woman;
        generateHumans(numberOfHumans, humans, new Vector3(900, 0, 900));
    }


    // Update is called once per frame
    public void generateHumans(int NumObjects, GameObject[] _humans, Vector3 area)
    {
        for (var i = 0; i < NumObjects; i++)
        {
            System.Random rand = new System.Random();
            int x = rand.Next(0, 2);
            GameObject _human = humans[x]; 
            Vector2 posi = new Vector2(Random.Range(0.1f,1.0f) * area.x, Random.Range(0.1f, 1.0f) * area.z);
            RaycastHit hit;
            float yofsset = 0;
            if (Physics.Raycast(new Vector3(posi.x, height, posi.y), -Vector3.up, out hit))
            {
                yofsset = height + 15 - hit.distance;
                realposi = new Vector3(posi.x,yofsset, posi.y);
                human = Instantiate(humans[x], realposi, _human.transform.rotation);
                human.transform.SetParent(gameObject.transform);
            }
        }
    }
}
