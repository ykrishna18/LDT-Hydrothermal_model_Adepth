/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Copyright (C) YEAR OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

\*---------------------------------------------------------------------------*/

#include "codedFunctionObjectTemplate.H"
#include "fvCFD.H"
#include "unitConversion.H"
#include "addToRunTimeSelectionTable.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

// * * * * * * * * * * * * * * Static Data Members * * * * * * * * * * * * * //

defineTypeNameAndDebug(calPlumeTFunctionObject, 0);

addRemovableToRunTimeSelectionTable
(
    functionObject,
    calPlumeTFunctionObject,
    dictionary
);


// * * * * * * * * * * * * * * * Global Functions  * * * * * * * * * * * * * //

extern "C"
{
    // dynamicCode:
    // SHA1 = 81e80fd6feb7fb612bf35eb465ca8ac805e76a7d
    //
    // unique function name that can be checked if the correct library version
    // has been loaded
    void calPlumeT_81e80fd6feb7fb612bf35eb465ca8ac805e76a7d(bool load)
    {
        if (load)
        {
            // code that can be explicitly executed after loading
        }
        else
        {
            // code that can be explicitly executed before unloading
        }
    }
}


// * * * * * * * * * * * * * * * Local Functions * * * * * * * * * * * * * * //

//{{{ begin localCode

//}}} end localCode


// * * * * * * * * * * * * * Private Member Functions  * * * * * * * * * * * //

const fvMesh& calPlumeTFunctionObject::mesh() const
{
    return refCast<const fvMesh>(obr_);
}


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

calPlumeTFunctionObject::calPlumeTFunctionObject
(
    const word& name,
    const Time& runTime,
    const dictionary& dict
)
:
    functionObjects::regionFunctionObject(name, runTime, dict)
{
    read(dict);
}


// * * * * * * * * * * * * * * * * Destructor  * * * * * * * * * * * * * * * //

calPlumeTFunctionObject::~calPlumeTFunctionObject()
{}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

bool calPlumeTFunctionObject::read(const dictionary& dict)
{
    if (false)
    {
        Info<<"read calPlumeT sha1: 81e80fd6feb7fb612bf35eb465ca8ac805e76a7d\n";
    }

//{{{ begin code
    
//}}} end code

    return true;
}


Foam::wordList calPlumeTFunctionObject::fields() const
{
    if (false)
    {
        Info<<"fields calPlumeT sha1: 81e80fd6feb7fb612bf35eb465ca8ac805e76a7d\n";
    }

    wordList fields;
//{{{ begin code
    
//}}} end code

    return fields;
}


bool calPlumeTFunctionObject::execute()
{
    if (false)
    {
        Info<<"execute calPlumeT sha1: 81e80fd6feb7fb612bf35eb465ca8ac805e76a7d\n";
    }

//{{{ begin code
    
//}}} end code

    return true;
}


bool calPlumeTFunctionObject::write()
{
    if (false)
    {
        Info<<"write calPlumeT sha1: 81e80fd6feb7fb612bf35eb465ca8ac805e76a7d\n";
    }

//{{{ begin code
    #line 53 "/home/ykrishna/HydrothermalFoam_cases/test_fault_10m/system/controlDict/functions/calPlumeT"
//get maximum tempeature on the top boundary
            label patchID = mesh().boundaryMesh().findPatchID("top"); 
            const volScalarField& T = mesh().lookupObject<volScalarField>("T");
            //const volScalarField& mu = mesh().lookupObject<volScalarField>("mu");
            //const volScalarField& Cp = mesh().lookupObject<volScalarField>("Cp");
            //const volScalarField& rho = mesh().lookupObject<volScalarField>("rho");
            //const surfaceScalarField& phi = mesh().lookupObject<surfaceScalarField>("phi");
            //const volScalarField& h = mesh().lookupObject<volScalarField>("enthalpy");
            //double kr = 2.0;
            // calculate local Rayleigh number 
            //volScalarField Ra_L("LocalRayleigh",mag(fvc::div(phi, h) / (kr*fvc::laplacian(T))));
            // write properties to output files
            //mu.write(); Cp.write(); h.write(); Ra_L.write();
            // write vent temperature
            std::ofstream fout("ventT.txt",std::ofstream::app);
            // Info<<"Plume Temperature: "<<mesh().time().value()/31536000<<"\t"<<Foam::gMax(T.boundaryField()[patchID])-273.15<<" C"<<endl;
            fout<<mesh().time().value()/31536000<<"\t"<<Foam::gMax(T.boundaryField()[patchID])-273.15<<std::endl;
            fout.close();
//}}} end code

    return true;
}


bool calPlumeTFunctionObject::end()
{
    if (false)
    {
        Info<<"end calPlumeT sha1: 81e80fd6feb7fb612bf35eb465ca8ac805e76a7d\n";
    }

//{{{ begin code
    
//}}} end code

    return true;
}


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam

// ************************************************************************* //

