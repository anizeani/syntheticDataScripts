using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DelayCameraSweep : MonoBehaviour
{
    private int _height = 30;

    public int height { get => _height; set => _height = value; }     // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(Wait(5));
    }

    private IEnumerator Wait(int seconds)
    {
        yield return new WaitForSeconds(seconds);
        var sweep = Camera.main.gameObject.AddComponent<CameraSweepAt90>();
        sweep.height = this.height;
        //gameObject.AddComponent<CameraSweepAt90>();
    }
}
