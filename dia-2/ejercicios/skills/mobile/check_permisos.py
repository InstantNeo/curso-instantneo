"""Skills para verificación de permisos en aplicaciones móviles"""

from instantneo.skills import skill


@skill(
    description="Verifica qué permisos necesita una funcionalidad de app móvil y si están configurados",
    tags=["mobile", "debugging", "permissions"]
)
def verificar_permisos_requeridos(funcionalidad: str, plataforma: str = "Android") -> dict:
    """
    Verifica los permisos necesarios para una funcionalidad específica de app móvil.

    Args:
        funcionalidad: Funcionalidad a verificar (ej: "camara", "ubicacion", "notificaciones")
        plataforma: Plataforma móvil (Android o iOS)

    Returns:
        Diccionario con permisos necesarios y configuración
    """
    # Base de conocimiento de permisos por funcionalidad
    permisos_android = {
        "camara": {
            "permisos": ["android.permission.CAMERA"],
            "permisos_runtime": True,
            "desde_api": 23,
            "manifest": '<uses-permission android:name="android.permission.CAMERA" />',
            "codigo_ejemplo": 'ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.CAMERA), REQUEST_CODE)'
        },
        "ubicacion": {
            "permisos": [
                "android.permission.ACCESS_FINE_LOCATION",
                "android.permission.ACCESS_COARSE_LOCATION"
            ],
            "permisos_runtime": True,
            "desde_api": 23,
            "manifest": '<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />',
            "codigo_ejemplo": 'FusedLocationProviderClient - requiere Google Play Services'
        },
        "almacenamiento": {
            "permisos": [
                "android.permission.READ_EXTERNAL_STORAGE",
                "android.permission.WRITE_EXTERNAL_STORAGE"
            ],
            "permisos_runtime": True,
            "desde_api": 23,
            "manifest": '<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />',
            "nota_adicional": "Android 11+ requiere uso de Scoped Storage"
        },
        "notificaciones": {
            "permisos": ["android.permission.POST_NOTIFICATIONS"],
            "permisos_runtime": True,
            "desde_api": 33,
            "manifest": '<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />',
            "codigo_ejemplo": 'NotificationManagerCompat.from(context).notify()'
        }
    }

    permisos_ios = {
        "camara": {
            "permisos": ["NSCameraUsageDescription"],
            "archivo_config": "Info.plist",
            "ejemplo_plist": '<key>NSCameraUsageDescription</key><string>Necesitamos acceso a la cámara para...</string>',
            "codigo_ejemplo": 'AVCaptureDevice.requestAccess(for: .video)'
        },
        "ubicacion": {
            "permisos": [
                "NSLocationWhenInUseUsageDescription",
                "NSLocationAlwaysUsageDescription"
            ],
            "archivo_config": "Info.plist",
            "ejemplo_plist": '<key>NSLocationWhenInUseUsageDescription</key><string>Necesitamos tu ubicación para...</string>',
            "codigo_ejemplo": 'CLLocationManager().requestWhenInUseAuthorization()'
        },
        "notificaciones": {
            "permisos": ["Push Notifications Capability"],
            "archivo_config": "Capabilities en Xcode",
            "codigo_ejemplo": 'UNUserNotificationCenter.current().requestAuthorization()',
            "nota_adicional": "Requiere certificado APNs configurado"
        }
    }

    funcionalidad_lower = funcionalidad.lower()

    if plataforma.lower() == "android":
        info = permisos_android.get(funcionalidad_lower)
        if not info:
            return {
                "error": f"Funcionalidad '{funcionalidad}' no encontrada en base de datos",
                "funcionalidades_disponibles": list(permisos_android.keys())
            }

        return {
            "plataforma": "Android",
            "funcionalidad": funcionalidad,
            "permisos_requeridos": info["permisos"],
            "requiere_runtime_permission": info["permisos_runtime"],
            "desde_api_level": info.get("desde_api"),
            "configuracion_manifest": info.get("manifest"),
            "ejemplo_codigo": info.get("codigo_ejemplo"),
            "nota_adicional": info.get("nota_adicional", ""),
            "pasos_implementacion": [
                "1. Agregar permisos al AndroidManifest.xml",
                "2. Solicitar permisos en runtime (API 23+)",
                "3. Manejar respuesta del usuario (granted/denied)",
                "4. Implementar fallback si se niega el permiso"
            ]
        }

    elif plataforma.lower() == "ios":
        info = permisos_ios.get(funcionalidad_lower)
        if not info:
            return {
                "error": f"Funcionalidad '{funcionalidad}' no encontrada en base de datos",
                "funcionalidades_disponibles": list(permisos_ios.keys())
            }

        return {
            "plataforma": "iOS",
            "funcionalidad": funcionalidad,
            "keys_requeridas": info["permisos"],
            "archivo_configuracion": info["archivo_config"],
            "ejemplo_configuracion": info.get("ejemplo_plist"),
            "ejemplo_codigo": info.get("codigo_ejemplo"),
            "nota_adicional": info.get("nota_adicional", ""),
            "pasos_implementacion": [
                "1. Agregar keys de privacidad al Info.plist",
                "2. Incluir descripción clara del uso del permiso",
                "3. Solicitar permiso programáticamente",
                "4. Revisar estado del permiso antes de usar funcionalidad"
            ]
        }

    return {
        "error": f"Plataforma '{plataforma}' no soportada",
        "plataformas_disponibles": ["Android", "iOS"]
    }


@skill(
    description="Diagnostica problemas comunes relacionados con permisos en apps móviles",
    tags=["mobile", "debugging", "permissions", "troubleshooting"]
)
def diagnosticar_problema_permisos(
    descripcion_problema: str,
    plataforma: str = "Android"
) -> dict:
    """
    Diagnostica y sugiere soluciones para problemas comunes de permisos.

    Args:
        descripcion_problema: Descripción del problema que está ocurriendo
        plataforma: Plataforma móvil (Android o iOS)

    Returns:
        Diccionario con diagnóstico y soluciones
    """
    problemas_comunes = {
        "Android": {
            "permiso denegado": {
                "causas": [
                    "Usuario denegó el permiso en el diálogo",
                    "Permiso no declarado en AndroidManifest.xml",
                    "No se solicitó runtime permission (API 23+)"
                ],
                "soluciones": [
                    "Verificar que el permiso esté en AndroidManifest.xml",
                    "Solicitar permiso con requestPermissions()",
                    "Explicar al usuario por qué necesitas el permiso",
                    "Redirigir a Settings si el usuario marcó 'No preguntar de nuevo'"
                ],
                "codigo_util": "if (shouldShowRequestPermissionRationale()) { /* Mostrar explicación */ }"
            },
            "camara no funciona": {
                "causas": [
                    "Falta permiso CAMERA en manifest",
                    "Usuario denegó el permiso",
                    "Otra app está usando la cámara"
                ],
                "soluciones": [
                    "Verificar <uses-permission android:name=\"android.permission.CAMERA\" />",
                    "Solicitar permiso en runtime",
                    "Verificar que no haya conflictos con otras apps",
                    "Comprobar que el dispositivo tenga cámara disponible"
                ]
            },
            "ubicacion no disponible": {
                "causas": [
                    "GPS desactivado",
                    "Permisos de ubicación denegados",
                    "Servicios de Google Play no disponibles"
                ],
                "soluciones": [
                    "Verificar que el GPS esté activado",
                    "Solicitar ACCESS_FINE_LOCATION o ACCESS_COARSE_LOCATION",
                    "Usar LocationManager para verificar disponibilidad",
                    "Implementar fallback sin ubicación precisa"
                ]
            }
        },
        "iOS": {
            "permiso denegado": {
                "causas": [
                    "Falta descripción en Info.plist",
                    "Usuario denegó el permiso",
                    "Descripción poco clara del uso"
                ],
                "soluciones": [
                    "Agregar NSXXXUsageDescription al Info.plist",
                    "Usar texto descriptivo que explique el beneficio al usuario",
                    "Redirigir a Settings para cambiar permisos",
                    "Implementar graceful degradation si se niega"
                ],
                "codigo_util": "UIApplication.shared.open(URL(string: UIApplication.openSettingsURLString)!)"
            },
            "camara no funciona": {
                "causas": [
                    "Falta NSCameraUsageDescription",
                    "Usuario denegó acceso",
                    "Restricciones de privacidad activas"
                ],
                "soluciones": [
                    "Agregar NSCameraUsageDescription al Info.plist",
                    "Verificar authorizationStatus antes de usar",
                    "Solicitar acceso con requestAccess(for: .video)",
                    "Revisar Restrictions en Settings del dispositivo"
                ]
            },
            "notificaciones no llegan": {
                "causas": [
                    "Usuario no autorizó notificaciones",
                    "Certificado APNs mal configurado",
                    "App en modo Do Not Disturb"
                ],
                "soluciones": [
                    "Solicitar autorización con requestAuthorization()",
                    "Verificar certificado APNs en Apple Developer",
                    "Registrar para notificaciones remotas",
                    "Revisar configuración de notificaciones en Settings"
                ]
            }
        }
    }

    # Detectar el problema en la descripción
    descripcion_lower = descripcion_problema.lower()
    plataforma_info = problemas_comunes.get(plataforma, {})

    diagnostico_encontrado = None
    clave_problema = None

    for problema, info in plataforma_info.items():
        if problema in descripcion_lower:
            diagnostico_encontrado = info
            clave_problema = problema
            break

    if not diagnostico_encontrado:
        return {
            "plataforma": plataforma,
            "problema_detectado": "No se pudo detectar automáticamente",
            "sugerencia": "Revisa los problemas comunes listados",
            "problemas_comunes": list(plataforma_info.keys()),
            "recomendacion_general": [
                "Verificar logs del sistema",
                "Revisar configuración de permisos en Settings",
                "Comprobar que los permisos estén correctamente declarados"
            ]
        }

    return {
        "plataforma": plataforma,
        "problema_detectado": clave_problema,
        "causas_probables": diagnostico_encontrado["causas"],
        "soluciones_recomendadas": diagnostico_encontrado["soluciones"],
        "codigo_util": diagnostico_encontrado.get("codigo_util", ""),
        "documentacion": f"https://developer.{'android' if plataforma == 'Android' else 'apple'}.com/documentation"
    }
