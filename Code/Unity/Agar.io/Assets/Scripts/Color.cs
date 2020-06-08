//Gathering resources
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class Color : MonoBehaviour 
{
    //Create the list
    public List<Material> Mats = new List<Material>();

    void Awake()
    {
        //Change the color randomly
        GetComponent<Renderer>().material = Mats[Random.Range(0, Mats.Count)];
    }
}
